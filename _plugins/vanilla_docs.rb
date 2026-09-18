# Turns a tree of vanilla Markdown into Jekyll pages.
#
# Why this exists: Jekyll only renders a file that carries YAML front matter.
# A .md file without it is treated as a static file and copied through
# verbatim — it never becomes HTML. Since we want maintainers writing plain
# Markdown with no front matter, something has to supply what front matter
# normally would. This generator does, deriving it from the file itself:
#
#   title  <- the first H1 (which is then dropped, because the layout
#             renders the title itself)
#   toc    <- every H2/H3, with the anchor ids kramdown actually emitted
#   nav    <- the directory tree, ordered by optional NN- filename prefixes
#
# Runs under `jekyll build` on Actions (plugins are unavailable on the
# built-in GitHub Pages builder, which is one more reason we build on Actions).

module VanillaDocs
  SOURCE_DIR = "docs".freeze
  ORDER_PREFIX = /\A(\d+)[-_]/.freeze

  # Strips an optional NN- ordering prefix. "20-launch.md" sorts after
  # "10-accounts.md" but lands at /docs/getting-started/launch/.
  def self.split_order(basename)
    if (m = ORDER_PREFIX.match(basename))
      [m[1].to_i, basename.sub(ORDER_PREFIX, "")]
    else
      [9999, basename]
    end
  end

  def self.humanize(slug)
    slug.tr("-_", "  ").split(/\s+/).map { |w| w[0] ? w[0].upcase + w[1..] : w }.join(" ")
  end

  # Kramdown's GFM parser covers most of GitHub Flavored Markdown --
  # tables, strikethrough, task lists, fenced code, footnotes, and
  # duplicate-heading id suffixing all match GitHub. Two things it does
  # not do, both verified against a torture page:
  #
  #   * GitHub alert callouts (> [!NOTE]) come out as a blockquote with a
  #     literal "[!NOTE]" in the text
  #   * bare URLs are not turned into links
  #
  # Both are common in hand-written GFM, so they are fixed here rather than
  # left for maintainers to work around.
  module GFM
    ALERTS = %w[NOTE TIP IMPORTANT WARNING CAUTION].freeze

    # > [!WARNING]  ->  a canvas-scoped callout. Deliberately NOT Bootstrap's
    # .alert-warning / .alert-danger: Decorator's base.css has zero rules for
    # the -info/-warning/-danger families, so those render in stock Bootstrap
    # colors on a UC San Diego page.
    def self.transform_alerts(html)
      html.gsub(%r{<blockquote>\s*<p>\s*\[!(#{ALERTS.join("|")})\]\s*(?:<br\s*/?>)?\s*(.*?)</p>(.*?)</blockquote>}m) do
        kind  = Regexp.last_match(1)
        first = Regexp.last_match(2).to_s.strip
        rest  = Regexp.last_match(3).to_s.strip
        label = kind.capitalize
        body  = first.empty? ? "" : "<p>#{first}</p>"
        %(<div class="docs-note docs-note--#{kind.downcase}">) +
          %(<p class="docs-note__label">#{label}</p>#{body}#{rest}</div>)
      end
    end

    # Links bare http(s) URLs, skipping anything already inside an anchor,
    # inline code, a code block, or an attribute value. The split keeps those
    # regions as delimiters (odd indices) and only rewrites the text between.
    SKIP = %r{(<a\b.*?</a>|<code\b.*?</code>|<pre\b.*?</pre>|<[^>]+>)}m
    URL  = %r{\bhttps?://[^\s<>"']*[^\s<>"'.,;:!?)\]]}

    def self.autolink(html)
      html.split(SKIP).each_with_index.map do |seg, i|
        i.odd? ? seg : seg.gsub(URL) { |u| %(<a href="#{u}">#{u}</a>) }
      end.join
    end
  end

  class DocPage < Jekyll::Page
    attr_reader :order, :nav_dir

    def initialize(site, base, abs_path, root)
      @site = site
      @base = base
      rel = Pathname.new(abs_path).relative_path_from(Pathname.new(root)).to_s
      dirname = File.dirname(rel)
      dirname = "" if dirname == "."
      basename = File.basename(rel, ".md")

      @order, slug = VanillaDocs.split_order(basename)
      @nav_dir = dirname

      index = %w[index readme].include?(slug.downcase)
      @dir = index ? File.join("/", VanillaDocs::SOURCE_DIR, dirname)
                   : File.join("/", VanillaDocs::SOURCE_DIR, dirname, slug)
      @name = "index.html"

      process(@name)
      self.data = {}

      raw = File.read(abs_path, encoding: "utf-8")
      html = render_markdown(site, raw)
      html = GFM.transform_alerts(html)
      html = GFM.autolink(html)

      title, html = extract_and_strip_h1(html)
      data["title"] = title || VanillaDocs.humanize(slug)
      data["toc"] = extract_toc(html)
      data["layout"] = "two-column"
      data["source_path"] = File.join(VanillaDocs::SOURCE_DIR, rel)
      data["is_index"] = index

      # Content is already HTML, and the page is named .html, so Jekyll
      # will not run the Markdown converter over it a second time. That is
      # deliberate: the toc anchors below are read out of THIS html, so they
      # are the ids kramdown really emitted rather than a guess at its
      # slugging rules.
      self.content = html
    end

    private

    def render_markdown(site, raw)
      converter = site.find_converter_instance(Jekyll::Converters::Markdown)
      converter.convert(raw)
    end

    # The layout renders <h1>{{ page.title }}</h1>, so the document's own H1
    # is removed to avoid emitting two.
    def extract_and_strip_h1(html)
      m = html.match(%r{<h1[^>]*>(.*?)</h1>}m)
      return [nil, html] unless m
      [strip_tags(m[1]), html.sub(m[0], "")]
    end

    def extract_toc(html)
      html.scan(%r{<h([23])\s[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>}m).map do |level, id, inner|
        { "level" => level.to_i, "id" => id, "text" => strip_tags(inner) }
      end
    end

    def strip_tags(s)
      s.gsub(/<[^>]+>/, "").gsub(/\s+/, " ").strip
    end
  end

  class Generator < Jekyll::Generator
    safe false
    priority :high

    def generate(site)
      root = File.join(site.source, SOURCE_DIR)
      return unless Dir.exist?(root)

      pages = Dir.glob(File.join(root, "**", "*.md")).sort.map do |path|
        DocPage.new(site, site.source, path, root)
      end

      site.pages.concat(pages)
      site.data["docs_nav"] = build_nav(pages)
    end

    private

    # Groups pages by directory. A directory's own title comes from its
    # index/readme H1 when there is one, otherwise from the directory name.
    def build_nav(pages)
      by_dir = pages.group_by(&:nav_dir)

      top = (by_dir[""] || []).reject { |p| p.data["is_index"] }
      sections = by_dir.keys.reject(&:empty?).sort.map do |dir|
        entries = by_dir[dir]
        index = entries.find { |p| p.data["is_index"] }
        children = entries.reject { |p| p.data["is_index"] }
                          .sort_by { |p| [p.order, p.data["title"].to_s] }
        {
          "title" => index ? index.data["title"] : VanillaDocs.humanize(File.basename(dir)),
          "url" => index ? index.url : nil,
          "children" => children.map { |p| { "title" => p.data["title"], "url" => p.url } }
        }
      end

      top.sort_by { |p| [p.order, p.data["title"].to_s] }
         .map { |p| { "title" => p.data["title"], "url" => p.url, "children" => [] } } + sections
    end
  end
end
