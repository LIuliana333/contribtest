
import os
import sys
import json
import logging
import jinja2

log = logging.getLogger(__name__)


def list_files(folder_path):
    for name in os.listdir(folder_path):       #se parcurg fisierele/directoarele din folderul cu calea folder_path
        base, ext = os.path.splitext(name)     #imparte numele caii in base si ext (radacina si extensie)
        if ext != '.rst':                      #daca gaseste un fisier cu extensia .rst, trece la urmatorul fisier din folder
            continue
        yield os.path.join(folder_path, name)  #orice alt fisier gasit se pune in fisierul gasit anterior

def read_file(file_path):
    with open(file_path, 'rt') as f:           #f este un obiect fisier (se deschide fisierul pentru a fi citit, fisier tip text)
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':          #daca dupa ce se elimina spatiile de la inceputul si finalul liniei, aceasta este --- atunci 
                                               #nu mai avem de preluat informatii de tip metadata
                break
            raw_metadata += line               #se concateneaza liniile in raw_metadata
        content = ""
        for line in f:
            content += line                    #se concateneaza informatia propriu-zisa in content
    return json.loads(raw_metadata), content   #se returneaza dictionarul din metadata si continutul

def write_output(name, html):
    # TODO should not use sys.argv here, it breaks encapsulation              #"\" este caracter special"
    with open('.\\test\\'+os.path.join(sys.argv[2], name+'.html'),'w') as f:  # se deschide fisierul    .\test\[sys.argv[2]]\name.html                                                                                     # pentru a putea scrie in el ca e html
        f.write(html)

def generate_site(folder_path):
    log.info("Generating site from %r", folder_path)
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(folder_path + '\layout'))
    for file_path in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']
        template = jinja2_env.get_template(template_name)
        data = dict(metadata, content=content)
        html = template.render(**data)
        index = 0
        for caracter in file_path:   # pentru identificarea numelor fisierelor (numele se afla dupa "\") in scopul crearii caii fisierului
            if(caracter == '\\'):    #"\" este caracter special => "\\"
                break
            index += 1
        index += 1
        name = file_path[index:].strip('rst').strip('.')
        write_output(name, html)
        log.info("Writing %r with template %r", name, template_name)


def main():
    generate_site(sys.argv[1])


if __name__ == '__main__':
    logging.basicConfig()
    main()
