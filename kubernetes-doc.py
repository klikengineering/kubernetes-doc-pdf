import requests_html as rh
import os
# import pypandoc
import subprocess

def generate_directory_pdf(url, name, s=None):
    s = rh.HTMLSession() if not s else s
    r1 = s.get(url)

    html = ""
    anchors = r1.html.find('.td-sidebar-link')
    links = [a.absolute_links.pop() for a in anchors if a.element.tag == 'a']
    # dedup
    unique_links = []
    for i in links:
        if i not in unique_links:
            unique_links.append(i)
    links = unique_links
    links = filter(lambda href: href.startswith(url), links) # filter out links

    print("downloading...")
    cwd = os.getcwd()
    for l1 in links:
        r2 = s.get(l1)
        if div := r2.html.find('.td-content', first=True, clean=True):
            # except Exception as e:
            #     print(" failed!")
            #     print(e)
            # else:
            html += div.html
        with open(f"{cwd}/{name}.html", "wt") as f:
            f.write(html)

    print("generating pdf...")
    subprocess.run([f"{cwd}/weasy_print.sh", name])
    # try:
    #     output = pypandoc.convert_text(html, "pdf", format="html", outputfile="./{}.pdf".format(name), extra_args=['--pdf-engine=weasyprint', '--css=codeblock_wrap.css'])
    # except Exception as e:
    #     print(e)

if __name__ == '__main__':
    s = rh.HTMLSession()
    directories = [\
                   "Setup",
                   "Concepts",
                   "Tasks",
                   "Tutorials",
                   "Reference",
                   # "Getting-started-guides",  # same as setup
                   # "Admin",  # this direct to concepts
                   # "Imported",  # deprecated
                   ]
    directories_pairs = [
        (f"https://kubernetes.io/docs/{n.lower()}/", n) for n in directories
    ]
    for url, name in directories_pairs:
        print(name)
        generate_directory_pdf(url, name)
