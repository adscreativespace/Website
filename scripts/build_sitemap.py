"""Write sitemap.xml: static pages plus one URL per project (projects/*.md)."""
import os, datetime
SITE = "https://adscreativespace.com/"
today = datetime.date.today().isoformat()
static = [("", "1.0", "weekly"), ("projects.html", "0.9", "weekly"), ("services.html", "0.9", "monthly"),
          ("about.html", "0.8", "monthly"), ("gallery.html", "0.8", "weekly"), ("packages.html", "0.8", "monthly"),
          ("contact.html", "0.8", "yearly"), ("consultation.html", "0.7", "yearly")]
urls = [(SITE + p, pr, cf) for p, pr, cf in static]
for n in sorted(os.listdir("projects")):
    if n.endswith(".md"):
        urls.append((SITE + "project.html?slug=" + n[:-3], "0.7", "monthly"))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, pr, cf in urls:
    out.append(f"  <url><loc>{u.replace('&', '&amp;')}</loc><lastmod>{today}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>")
out.append("</urlset>")
open("sitemap.xml", "w").write("\n".join(out) + "\n")
print(len(urls), "urls")
