#!/usr/bin/env python3
"""Assemble the Sugarcoat Blogger XML theme from style.css and script.js."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "style.css").read_text(encoding="utf-8")
JS = (ROOT / "script.js").read_text(encoding="utf-8")

if "]]>" in CSS or "]]>" in JS:
    raise SystemExit("CDATA terminator found in CSS/JS")


def html_widget(widget_id, title="", content=""):
    return (
        f"\n          <b:widget id='{widget_id}' locked='false' title='{title}' type='HTML' version='2' visible='true'>\n"
        "            <b:widget-settings>\n"
        "              <b:widget-setting name='content'><![CDATA[" + content + "]]></b:widget-setting>\n"
        "            </b:widget-settings>\n"
        "            <b:includable id='main'>\n"
        "              <div class='widget-content'><data:content/></div>\n"
        "            </b:includable>\n"
        "          </b:widget>"
    )


ADSENSE_SIDEBAR = """<ins class="adsbygoogle"
     style="display:block;width:300px;height:250px"
     data-ad-client="ca-pub-6692939836499331"
     data-ad-slot="7633913202"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>"""

ADSENSE_BOTTOM = """<ins class="adsbygoogle"
     style="display:block;width:336px;height:280px"
     data-ad-client="ca-pub-6692939836499331"
     data-ad-slot="1008345394"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>"""


SUPER_IDS = [
    ("aboutPostAuthor", ""),
    ("addComments", ""),
    ("backLinks", " var='post'"),
    ("blogThisShare", ""),
    ("bylineByName", " var='byline'"),
    ("bylineRegion", " var='regionItems'"),
    ("commentAuthorAvatar", ""),
    ("commentDeleteIcon", " var='comment'"),
    ("commentForm", " var='post'"),
    ("commentFormIframeSrc", " var='post'"),
    ("commentItem", " var='comment'"),
    ("commentList", " var='comments'"),
    ("commentPicker", " var='post'"),
    ("comments", " var='post'"),
    ("commentsLink", ""),
    ("commentsLinkIframe", ""),
    ("commentsTitle", ""),
    ("defaultAdUnit", ""),
    ("emailPostIcon", ""),
    ("facebookShare", ""),
    ("feedLinks", ""),
    ("feedLinksBody", " var='links'"),
    ("googlePlusShare", ""),
    ("homePageLink", ""),
    ("iframeComments", " var='post'"),
    ("linkShare", ""),
    ("manageComments", ""),
    ("otherSharingButton", ""),
    ("platformShare", ""),
    ("postFooterAuthorProfile", " var='post'"),
    ("postLocation", ""),
    ("postMetadataJSON", ""),
    ("postMetadataJSONImage", ""),
    ("postMetadataJSONPublisher", ""),
    ("postPagination", ""),
    ("postReactions", " var='post'"),
    ("sharingButton", ""),
    ("sharingButtonContent", ""),
    ("sharingButtons", ""),
    ("sharingButtonsMenu", ""),
    ("sharingPlatformIcon", ""),
    ("threadedCommentForm", " var='post'"),
    ("threadedCommentJs", " var='post'"),
    ("threadedComments", " var='post'"),
    ("tooltipCss", ""),
]

super_blocks = []
for name, var in SUPER_IDS:
    data_attr = " data='post'" if "post" in var else ""
    if name in ("commentDeleteIcon",):
        data_attr = " data='comment'"
    if name in ("commentList",):
        data_attr = " data='comments'"
    if name in ("bylineByName",):
        data_attr = " data='byline'"
    if name in ("bylineRegion",):
        data_attr = " data='regionItems'"
    if name in ("feedLinksBody",):
        data_attr = " data='links'"
    super_blocks.append(
        f"            <b:includable id='{name}'{var}>\n"
        f"              <b:include{data_attr} name='super.{name}'/>\n"
        f"            </b:includable>"
    )
SUPER_XML = "\n".join(super_blocks)

XML = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<html b:css='false' b:defaultwidgetversion='2' b:layoutsVersion='3' b:responsive='true' b:templateVersion='1.2.0' expr:dir='data:blog.languageDirection' xmlns='http://www.w3.org/1999/xhtml' xmlns:b='http://www.google.com/2005/gml/b' xmlns:data='http://www.google.com/2005/gml/data' xmlns:expr='http://www.google.com/2005/gml/expr'>
<head>
  <b:include name='theme-head'/>
  <b:skin version='1.0.0'><![CDATA[/*
-----------------------------------------------
Blogger Template Style
Name:        Sugarcoat
Version:     1.0.0
-----------------------------------------------

<Variable name="keycolor" description="Main Color" type="color" default="#1f4f46" value="#1f4f46"/>
<Group description="Theme Colors" selector="body">
<Variable name="body.background.color" description="Background" type="color" default="#f6f6f4" value="#f6f6f4"/>
<Variable name="body.text.color" description="Text" type="color" default="#222222" value="#222222"/>
<Variable name="posts.title.color" description="Title" type="color" default="#111111" value="#111111"/>
<Variable name="main.color" description="Accent" type="color" default="#1f4f46" value="#1f4f46"/>
</Group>
<Variable name="body.text.font" description="Font" hideEditor="true" type="font" default="16px IBM Plex Sans KR, sans-serif" value="16px IBM Plex Sans KR, sans-serif"/>
<Variable name="posts.background.color" description="Surface" hideEditor="true" type="color" default="#ffffff" value="#ffffff"/>
*/

{CSS}
]]></b:skin>
  <b:template-skin>
    <b:variable default='960px' name='content.width' type='length' value='1080px'/>
    <b:variable default='0' name='main.column.left.width' type='length' value='0'/>
    <b:variable default='280px' name='main.column.right.width' type='length' value='280px'/>
  </b:template-skin>
</head>
<body>
  <b:class cond='data:view.isHomepage' name='home'/>
  <b:class cond='data:view.isPost' name='item'/>
  <b:class cond='data:view.isPage' name='static-page'/>
  <b:class cond='data:view.isArchive or data:view.search.label or data:view.search.query' name='archive'/>
  <b:class cond='data:view.isError' name='error404'/>

  <b:defaultmarkups>
    <b:defaultmarkup type='Common'>
      <b:includable id='widget-title'>
        <b:if cond='data:title != &quot;&quot;'>
          <div class='widget-title'><h3 class='title'><data:title/></h3></div>
        </b:if>
      </b:includable>
      <b:includable id='theme-head'>
        <meta content='width=device-width, initial-scale=1' name='viewport'/>
        <title><data:view.title.escaped/></title>
        <meta expr:content='data:view.description.escaped' name='description'/>
        <meta expr:content='&quot;text/html; charset=&quot; + data:blog.encoding' http-equiv='Content-Type'/>
        <meta content='#ffffff' name='theme-color'/>
        <meta content='ea6ff9bb5eb9b747dfe69fbe5d123c620bcf5dc8' name='naver-site-verification'/>
        <link expr:href='data:blog.blogspotFaviconUrl' rel='icon' type='image/x-icon'/>
        <link expr:href='data:view.url.canonical' rel='canonical'/>
        <link href='https://fonts.googleapis.com' rel='preconnect'/>
        <link crossorigin='anonymous' href='https://fonts.gstatic.com' rel='preconnect'/>
        <link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;600;700&amp;display=swap' rel='stylesheet'/>
        <script async='async' src='https://www.googletagmanager.com/gtag/js?id=G-KDJJ18MT54'/>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag(&#39;js&#39;, new Date());
          gtag(&#39;config&#39;, &#39;G-KDJJ18MT54&#39;);
        </script>
        <script async='async' crossorigin='anonymous' src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6692939836499331'/>
        <data:blog.feedLinks/>
        <data:blog.meTag/>
        <b:include name='openGraph'/>
      </b:includable>
      <b:includable id='openGraph'>
        <b:if cond='data:view.isHomepage'><meta content='website' property='og:type'/></b:if>
        <b:if cond='data:view.isSingleItem'><meta content='article' property='og:type'/></b:if>
        <meta expr:content='data:view.title.escaped' property='og:title'/>
        <meta expr:content='data:blog.url.canonical' property='og:url'/>
        <meta expr:content='data:view.description.escaped' property='og:description'/>
        <meta expr:content='data:blog.title.escaped' property='og:site_name'/>
        <b:if cond='data:view.featuredImage'>
          <meta expr:content='data:view.featuredImage' property='og:image'/>
          <meta expr:content='data:view.featuredImage' name='twitter:image'/>
        </b:if>
        <meta content='summary_large_image' name='twitter:card'/>
        <meta expr:content='data:view.title.escaped' name='twitter:title'/>
        <meta expr:content='data:view.description.escaped' name='twitter:description'/>
        <b:if cond='data:view.isHomepage'>
          <script type='application/ld+json'>{{&quot;@context&quot;:&quot;https://schema.org&quot;,&quot;@type&quot;:&quot;WebSite&quot;,&quot;name&quot;:&quot;<data:view.title.escaped/>&quot;,&quot;url&quot;:&quot;<data:view.url.canonical/>&quot;,&quot;potentialAction&quot;:{{&quot;@type&quot;:&quot;SearchAction&quot;,&quot;target&quot;:&quot;<data:view.url.canonical/>search?q={{search_term_string}}&quot;,&quot;query-input&quot;:&quot;required name=search_term_string&quot;}}}}</script>
        </b:if>
      </b:includable>
    </b:defaultmarkup>
    <b:defaultmarkup type='Header'>
      <b:includable id='main' var='this'>
        <a class='brand__title' expr:href='data:blog.homepageUrl.canonical'><data:title/></a>
      </b:includable>
    </b:defaultmarkup>
    <b:defaultmarkup type='PageList'>
      <b:includable id='main'><b:include name='content'/></b:includable>
      <b:includable id='content'>
        <ul>
          <b:loop values='data:links' var='link'>
            <li>
              <b:class cond='data:link.isCurrentPage' name='selected'/>
              <a expr:href='data:link.target'><data:link.title/></a>
            </li>
          </b:loop>
        </ul>
      </b:includable>
    </b:defaultmarkup>
    <b:defaultmarkup type='BlogSearch'>
      <b:includable id='main'><b:include name='content'/></b:includable>
      <b:includable id='content'>
        <form class='search-form' expr:action='data:blog.searchUrl' role='search'>
          <b:attr cond='not data:view.isPreview' name='target' value='_top'/>
          <b:include name='urlParamsAsFormInput'/>
          <input autocomplete='off' class='search-input' expr:aria-label='data:messages.searchThisBlog' expr:placeholder='data:messages.searchThisBlog' expr:value='data:view.isSearch ? data:view.search.query.escaped : &quot;&quot;' name='q'/>
          <input class='search-action' expr:value='data:messages.search.escaped' type='submit'/>
        </form>
      </b:includable>
    </b:defaultmarkup>
    <b:defaultmarkup type='Label'>
      <b:includable id='main'>
        <b:include name='widget-title'/>
        <div class='widget-content'>
          <ul>
            <b:loop values='data:labels' var='label'>
              <li>
                <a expr:href='data:label.url'><data:label.name/> <span>(<data:label.count/>)</span></a>
              </li>
            </b:loop>
          </ul>
        </div>
      </b:includable>
    </b:defaultmarkup>
    <b:defaultmarkup type='PopularPosts'>
      <b:includable id='main' var='this'>
        <b:include name='widget-title'/>
        <div class='widget-content'>
          <ol>
            <b:loop values='data:posts' var='post'>
              <li><a expr:href='data:post.url'><data:post.title/></a></li>
            </b:loop>
          </ol>
        </div>
      </b:includable>
    </b:defaultmarkup>
    <b:defaultmarkup type='BlogArchive'>
      <b:includable id='main' var='this'>
        <b:include name='widget-title'/>
        <div class='widget-content'>
          <ul>
            <b:loop values='data:data' var='i'>
              <li><a expr:href='data:i.url'><data:i.name/></a></li>
            </b:loop>
          </ul>
        </div>
      </b:includable>
    </b:defaultmarkup>
  </b:defaultmarkups>

  <b:include data='blog' name='google-analytics'/>
  <a class='skip-link' href='#content'>본문 바로가기</a>
  <div class='reading-progress' aria-hidden='true'><span/></div>

  <header class='site-header'>
    <div class='site-header__inner'>
      <div class='brand'>
        <b:section id='header' maxwidgets='1' name='블로그 제목' showaddelement='no'>
          <b:widget id='Header1' locked='true' title='핫딜포페어런츠' type='Header' version='2' visible='true'>
            <b:widget-settings>
              <b:widget-setting name='displayUrl'/>
              <b:widget-setting name='displayHeight'>0</b:widget-setting>
              <b:widget-setting name='sectionWidth'>-1</b:widget-setting>
              <b:widget-setting name='useImage'>false</b:widget-setting>
              <b:widget-setting name='shrinkToFit'>true</b:widget-setting>
              <b:widget-setting name='imagePlacement'>REPLACE</b:widget-setting>
              <b:widget-setting name='displayWidth'>0</b:widget-setting>
            </b:widget-settings>
            <b:includable id='main' var='this'>
              <a class='brand__title' expr:href='data:blog.homepageUrl.canonical'><data:title/></a>
            </b:includable>
            <b:includable id='description'><b:comment>hidden</b:comment></b:includable>
            <b:includable id='title'>
              <a class='brand__title' expr:href='data:blog.homepageUrl.canonical'><data:title/></a>
            </b:includable>
            <b:includable id='image'>
              <a class='brand__title' expr:href='data:blog.homepageUrl.canonical'><img expr:alt='data:title' expr:src='data:image'/></a>
            </b:includable>
            <b:includable id='behindImageStyle'><b:comment>unused</b:comment></b:includable>
          </b:widget>
        </b:section>
      </div>
      <button class='icon-button mobile-menu-button' data-menu-toggle='true' type='button' aria-label='메뉴 열기' aria-expanded='false'>
        <span/><span/><span/>
      </button>
      <nav class='site-nav' data-site-nav='true' aria-label='메뉴'>
        <b:section id='header-nav' maxwidgets='1' name='상단 메뉴' showaddelement='yes'>
          <b:widget id='PageList1' locked='false' title='페이지 목록' type='PageList' version='2' visible='true'>
            <b:widget-settings>
              <b:widget-setting name='pageListJson'><![CDATA[{{"home": {{"href": "/", "position": 0, "title": "홈"}}}}]]></b:widget-setting>
              <b:widget-setting name='homeTitle'>홈</b:widget-setting>
              <b:widget-setting name='homeLink'>true</b:widget-setting>
            </b:widget-settings>
            <b:includable id='main'><b:include name='content'/></b:includable>
            <b:includable id='content'>
              <ul>
                <b:loop values='data:links' var='link'>
                  <li>
                    <b:class cond='data:link.isCurrentPage' name='selected'/>
                    <a expr:href='data:link.target'><data:link.title/></a>
                  </li>
                </b:loop>
              </ul>
            </b:includable>
          </b:widget>
        </b:section>
      </nav>
      <div class='header-actions'>
        <b:section id='header-search' maxwidgets='1' name='검색' showaddelement='no'>
          <b:widget id='BlogSearch1' locked='true' title='검색' type='BlogSearch' version='2' visible='true'>
            <b:includable id='main'><b:include name='content'/></b:includable>
            <b:includable id='content'>
              <form class='search-form' expr:action='data:blog.searchUrl' role='search'>
                <b:attr cond='not data:view.isPreview' name='target' value='_top'/>
                <b:include name='urlParamsAsFormInput'/>
                <input autocomplete='off' expr:aria-label='data:messages.searchThisBlog' expr:placeholder='data:messages.searchThisBlog' expr:value='data:view.isSearch ? data:view.search.query.escaped : &quot;&quot;' name='q'/>
                <input expr:value='data:messages.search.escaped' type='submit'/>
              </form>
            </b:includable>
          </b:widget>
        </b:section>
      </div>
    </div>
  </header>

  <div class='site-shell'>
    <main class='site-main' id='content'>
      <b:if cond='data:view.isMultipleItems'>
        <div class='ad-slot ad-slot--list-top' aria-label='목록 상단 광고'><span class='ad-label'>AD</span></div>
      </b:if>

      <b:section class='main' id='main' maxwidgets='1' name='본문' showaddelement='no'>
        <b:widget id='Blog1' locked='true' title='블로그 게시물' type='Blog' version='2' visible='true'>
          <b:widget-settings>
            <b:widget-setting name='commentLabel'>댓글</b:widget-setting>
            <b:widget-setting name='showShareButtons'>false</b:widget-setting>
            <b:widget-setting name='authorLabel'>작성자</b:widget-setting>
            <b:widget-setting name='style.unittype'>TextAndImage</b:widget-setting>
            <b:widget-setting name='showAuthorProfile'>false</b:widget-setting>
            <b:widget-setting name='style.layout'>1x1</b:widget-setting>
            <b:widget-setting name='showLocation'>false</b:widget-setting>
            <b:widget-setting name='showTimestamp'>true</b:widget-setting>
            <b:widget-setting name='postsPerAd'>3</b:widget-setting>
            <b:widget-setting name='showDateHeader'>false</b:widget-setting>
            <b:widget-setting name='showCommentLink'>true</b:widget-setting>
            <b:widget-setting name='showAuthor'>true</b:widget-setting>
            <b:widget-setting name='showLabels'>true</b:widget-setting>
            <b:widget-setting name='postLabelsLabel'>라벨</b:widget-setting>
            <b:widget-setting name='showBacklinks'>false</b:widget-setting>
            <b:widget-setting name='showInlineAds'>false</b:widget-setting>
            <b:widget-setting name='showReactions'>false</b:widget-setting>
          </b:widget-settings>
          <b:includable id='main' var='this'>
            <b:include name='searchMessage'/>
            <div class='blog-posts hfeed'>
              <b:class cond='data:view.isMultipleItems' name='post-list'/>
              <b:attr cond='data:view.isMultipleItems' name='data-post-list' value='true'/>
              <b:loop index='i' values='data:posts' var='post'>
                <b:include data='post' name='postCommentsAndAd'/>
              </b:loop>
            </div>
            <b:include cond='data:view.isMultipleItems' name='indexBlogPager'/>
          </b:includable>
          <b:includable id='searchMessage'>
            <b:if cond='data:view.search.query or data:view.search.label or data:view.isArchive'>
              <section class='archive-head queryMessage'>
                <h1>
                  <b:if cond='data:view.search.query'><data:view.search.resultsMessageHtml/></b:if>
                  <b:if cond='data:view.search.label'><data:view.search.resultsMessageHtml/></b:if>
                  <b:if cond='data:view.isArchive'><data:view.archive.rangeMessage/></b:if>
                </h1>
              </section>
            </b:if>
            <b:if cond='data:view.isError'>
              <div class='errorWrap'>
                <h1>페이지를 찾을 수 없습니다</h1>
                <p><a expr:href='data:blog.homepageUrl'>홈으로 돌아가기</a></p>
              </div>
            </b:if>
          </b:includable>
          <b:includable id='postCommentsAndAd' var='post'>
            <article class='hentry'>
              <b:class cond='data:view.isMultipleItems' name='index-post post-card'/>
              <b:class cond='data:view.isSingleItem' name='item-post article'/>
              <b:include data='post' name='post'/>
            </article>
            <b:if cond='data:view.isSingleItem and data:post.allowComments'>
              <section class='comments-panel'>
                <b:include data='post' name='commentPicker'/>
              </section>
            </b:if>
          </b:includable>
          <b:includable id='post' var='post'>
            <b:if cond='data:view.isMultipleItems'><b:include data='post' name='indexPost'/></b:if>
            <b:if cond='data:view.isSingleItem'><b:include data='post' name='itemPost'/></b:if>
          </b:includable>
          <b:includable id='indexPost' var='post'>
            <a class='post-card__thumb post-image-link' expr:href='data:post.url'>
              <b:if cond='data:post.featuredImage'>
                <img class='post-thumb' expr:alt='data:post.title' expr:src='resizeImage(data:post.featuredImage, 480, &quot;3:2&quot;)' loading='lazy'/>
              </b:if>
            </a>
            <div class='post-card__body post-info'>
              <b:if cond='data:post.labels'>
                <a class='post-card__label' expr:href='data:post.labels.first.url'><data:post.labels.first.name/></a>
              </b:if>
              <h2 class='post-title'><a expr:href='data:post.url'><data:post.title/></a></h2>
              <p class='post-snippet'><b:eval expr='data:post.snippets.short snippet {{ length: 110 }}'/></p>
              <div class='post-card__meta post-meta'>
                <time expr:datetime='data:post.date.iso8601'><data:post.date/></time>
              </div>
            </div>
          </b:includable>
          <b:includable id='itemPost' var='post'>
            <header class='article-header'>
              <b:if cond='data:post.labels'>
                <a class='article-label' expr:href='data:post.labels.first.url'><data:post.labels.first.name/></a>
              </b:if>
              <h1 class='post-title'><data:post.title/></h1>
              <div class='article-meta post-meta'>
                <time expr:datetime='data:post.date.iso8601'><data:post.date/></time>
                <span><data:post.author.name/></span>
              </div>
            </header>
            <div class='ad-slot ad-slot--article-top' aria-label='본문 상단 광고'><span class='ad-label'>AD</span></div>
            <nav class='article-toc' data-toc='true' aria-label='목차'>
              <div class='article-toc__title'>목차</div>
              <ol data-toc-list='true'/>
            </nav>
            <div class='post-body article-body' data-article-body='true' expr:id='&quot;post-body-&quot; + data:post.id'>
              <data:post.body/>
            </div>
            <template id='article-middle-ad-template'>
              <div class='ad-slot ad-slot--article-middle' data-auto-ad='middle' aria-label='본문 중간 광고'><span class='ad-label'>AD</span></div>
            </template>
            <div class='ad-slot ad-slot--article-bottom' aria-label='본문 하단 광고'><span class='ad-label'>AD</span></div>
            <b:if cond='data:post.labels'>
              <section class='article-labels'>
                <b:loop values='data:post.labels' var='label'>
                  <a expr:href='data:label.url' rel='tag'><data:label.name/></a>
                </b:loop>
              </section>
            </b:if>
            <section class='article-actions'>
              <button data-copy-link='true' type='button'>링크 복사</button>
              <button data-native-share='true' type='button'>공유하기</button>
            </section>
            <nav class='post-nav'>
              <b:if cond='data:newerPageUrl'>
                <a expr:href='data:newerPageUrl'><span>다음 글</span><p><data:messages.newer/></p></a>
                <b:else/>
                <a class='is-empty'><span>다음 글</span><p>없음</p></a>
              </b:if>
              <b:if cond='data:olderPageUrl'>
                <a expr:href='data:olderPageUrl'><span>이전 글</span><p><data:messages.older/></p></a>
                <b:else/>
                <a class='is-empty'><span>이전 글</span><p>없음</p></a>
              </b:if>
            </nav>
          </b:includable>
          <b:includable id='indexBlogPager'>
            <nav class='pager blog-pager' id='blog-pager'>
              <b:if cond='data:newerPageUrl'>
                <a class='blog-pager-newer-link' expr:href='data:newerPageUrl'><data:messages.newer/></a>
              </b:if>
              <b:if cond='data:olderPageUrl'>
                <a class='blog-pager-older-link' expr:href='data:olderPageUrl'><data:messages.older/></a>
              </b:if>
            </nav>
          </b:includable>
          <b:includable id='headerByline' var='post'>
            <div class='post-meta'>
              <b:include data='post' name='postAuthor'/>
              <b:include data='post' name='postTimestamp'/>
            </div>
          </b:includable>
          <b:includable id='footerBylines' var='post'><b:include data='post' name='postLabels'/></b:includable>
          <b:includable id='postAuthor' var='post'><span class='post-author'><data:post.author.name/></span></b:includable>
          <b:includable id='postTimestamp' var='post'><time class='post-date' expr:datetime='data:post.date.iso8601'><data:post.date/></time></b:includable>
          <b:includable id='postTitle' var='post'>
            <b:if cond='data:view.isMultipleItems'><h2 class='post-title'><a expr:href='data:post.url'><data:post.title/></a></h2></b:if>
            <b:if cond='data:view.isSingleItem'><h1 class='post-title'><data:post.title/></h1></b:if>
          </b:includable>
          <b:includable id='postHeader' var='post'><b:include data='post' name='postTitle'/></b:includable>
          <b:includable id='postBody' var='post'><div class='post-body'><data:post.body/></div></b:includable>
          <b:includable id='postBodySnippet' var='post'><b:include data='post' name='postBody'/></b:includable>
          <b:includable id='postSummary' var='post'><p class='post-snippet'><b:eval expr='data:post.snippets.short snippet {{ length: 110 }}'/></p></b:includable>
          <b:includable id='postJumpLink' var='post'><a class='read-more' expr:href='data:post.url'>더 보기</a></b:includable>
          <b:includable id='postLabels' var='post'>
            <b:if cond='data:post.labels'>
              <div class='article-labels'>
                <b:loop values='data:post.labels' var='label'><a expr:href='data:label.url' rel='tag'><data:label.name/></a></b:loop>
              </div>
            </b:if>
          </b:includable>
          <b:includable id='postCategory' var='post'>
            <b:if cond='data:post.labels'><a class='post-card__label' expr:href='data:post.labels.first.url'><data:post.labels.first.name/></a></b:if>
          </b:includable>
          <b:includable id='postFeaturedImage' var='post'>
            <a class='post-card__thumb' expr:href='data:post.url'>
              <b:if cond='data:post.featuredImage'>
                <img class='post-thumb' expr:alt='data:post.title' expr:src='resizeImage(data:post.featuredImage, 480, &quot;3:2&quot;)'/>
              </b:if>
            </a>
          </b:includable>
          <b:includable id='postFooter' var='post'><b:comment>handled in itemPost</b:comment></b:includable>
          <b:includable id='postShareButtons' var='post'><b:comment>custom buttons</b:comment></b:includable>
          <b:includable id='postRelated' var='post'><b:comment>unused</b:comment></b:includable>
          <b:includable id='postShortMeta'><b:comment>unused</b:comment></b:includable>
          <b:includable id='postBreadcrumbs' var='post'><b:comment>unused</b:comment></b:includable>
          <b:includable id='postMeta' var='post'><b:comment>unused</b:comment></b:includable>
          <b:includable id='postCommentsLink'><b:comment>unused</b:comment></b:includable>
          <b:includable id='postNavigation' var='post'><b:comment>unused</b:comment></b:includable>
          <b:includable id='homePostsHeadline'><b:comment>unused</b:comment></b:includable>
          <b:includable id='inlineAd' var='post'><b:comment>manual slots</b:comment></b:includable>
          <b:includable id='messagesJs'><b:comment>unused</b:comment></b:includable>
          <b:includable id='nextPageLink'><b:comment>unused</b:comment></b:includable>
          <b:includable id='previousPageLink'><b:comment>unused</b:comment></b:includable>
          <b:includable id='threadedCommentsDisqus' var='post'><b:comment>disabled</b:comment></b:includable>
{SUPER_XML}
        </b:widget>
      </b:section>

      <b:if cond='data:view.isMultipleItems'>
        <template id='list-ad-template'>
          <div class='ad-slot ad-slot--list-middle' data-auto-ad='list' aria-label='목록 중간 광고'><span class='ad-label'>AD</span></div>
        </template>
        <div class='ad-slot ad-slot--list-bottom' aria-label='목록 하단 광고'><span class='ad-label'>AD</span></div>
      </b:if>
    </main>

    <aside class='site-sidebar'>
      <div class='sidebar-sticky'>
        <div class='ad-slot ad-slot--sidebar' aria-label='사이드바 광고'><span class='ad-label'>AD</span></div>
        <b:section class='sidebar' id='sidebar' name='사이드바' showaddelement='yes'>
          <b:widget id='Label1' locked='false' title='라벨' type='Label' version='2' visible='true'>
            <b:widget-settings>
              <b:widget-setting name='sorting'>ALPHA</b:widget-setting>
              <b:widget-setting name='display'>LIST</b:widget-setting>
              <b:widget-setting name='selectedLabelsList'/>
              <b:widget-setting name='showType'>ALL</b:widget-setting>
              <b:widget-setting name='showFreqNumbers'>true</b:widget-setting>
            </b:widget-settings>
            <b:includable id='main'>
              <section class='sidebar-widget'>
                <b:include name='widget-title'/>
                <div class='widget-content'>
                  <ul>
                    <b:loop values='data:labels' var='label'>
                      <li><a expr:href='data:label.url'><data:label.name/> (<data:label.count/>)</a></li>
                    </b:loop>
                  </ul>
                </div>
              </section>
            </b:includable>
          </b:widget>
          <b:widget id='PopularPosts1' locked='false' title='인기 글' type='PopularPosts' version='2' visible='true'>
            <b:widget-settings>
              <b:widget-setting name='numItemsToShow'>5</b:widget-setting>
              <b:widget-setting name='showThumbnails'>false</b:widget-setting>
              <b:widget-setting name='showSnippets'>false</b:widget-setting>
            </b:widget-settings>
            <b:includable id='main' var='this'>
              <section class='sidebar-widget'>
                <b:include name='widget-title'/>
                <div class='widget-content'>
                  <ol>
                    <b:loop values='data:posts' var='post'>
                      <li><a expr:href='data:post.url'><data:post.title/></a></li>
                    </b:loop>
                  </ol>
                </div>
              </section>
            </b:includable>
          </b:widget>
        </b:section>
      </div>
    </aside>
  </div>

  <button class='floating-toc-button' data-mobile-toc-toggle='true' type='button'>목차</button>
  <div class='mobile-toc' data-mobile-toc='true' hidden='hidden'>
    <div class='mobile-toc__panel'>
      <div class='mobile-toc__head'>
        <strong>목차</strong>
        <button data-mobile-toc-close='true' type='button'>닫기</button>
      </div>
      <ol data-mobile-toc-list='true'/>
    </div>
  </div>
  <div class='mobile-sticky-ad' data-mobile-sticky-ad='true' hidden='hidden'>
    <button data-mobile-ad-close='true' type='button'>닫기</button>
    <div class='ad-slot ad-slot--mobile-sticky' aria-label='모바일 하단 광고'><span class='ad-label'>AD</span></div>
  </div>

  <footer class='site-footer'>
    <p><a expr:href='data:blog.homepageUrl'><data:blog.title/></a></p>
    <b:section id='footer' name='푸터' showaddelement='yes'/>
  </footer>

  <div id='ad-sources'>
    <b:section id='ad-article-top' maxwidgets='1' name='본문 상단 광고' showaddelement='yes'>{html_widget('HTMLAdTop')}</b:section>
    <b:section id='ad-article-middle' maxwidgets='1' name='본문 중간 광고' showaddelement='yes'>{html_widget('HTMLAdMiddle')}</b:section>
    <b:section id='ad-article-bottom' maxwidgets='1' name='본문 하단 광고' showaddelement='yes'>{html_widget('HTMLAdBottom', '', ADSENSE_BOTTOM)}</b:section>
    <b:section id='ad-sidebar' maxwidgets='1' name='사이드바 광고' showaddelement='yes'>{html_widget('HTMLAdSidebar', '', ADSENSE_SIDEBAR)}</b:section>
    <b:section id='ad-list-top' maxwidgets='1' name='목록 상단 광고' showaddelement='yes'>{html_widget('HTMLAdListTop')}</b:section>
    <b:section id='ad-list-middle' maxwidgets='1' name='목록 중간 광고' showaddelement='yes'>{html_widget('HTMLAdListMiddle')}</b:section>
    <b:section id='ad-list-bottom' maxwidgets='1' name='목록 하단 광고' showaddelement='yes'>{html_widget('HTMLAdListBottom')}</b:section>
    <b:section id='ad-mobile-sticky' maxwidgets='1' name='모바일 하단 고정 광고' showaddelement='yes'>{html_widget('HTMLAdMobile')}</b:section>
  </div>

  <script>
  window.sugarcoatConfig = {{
    articleMiddleAdAfterHeading: 2,
    listAdAfterItem: 4,
    showAdPlaceholders: false,
    enableMobileStickyAd: false
  }};
  </script>
  <script type='text/javascript'>
  //<![CDATA[
{JS}
  //]]>
  </script>
</body>
</html>
"""

out = ROOT / "sugarcoat_blogger_theme.xml"
out.write_text(XML, encoding="utf-8")
print(f"Wrote {out} ({out.stat().st_size} bytes)")
