from Core import Config
from os import path
from lxml import etree
import sys

def append(image,filename:str):
    html_save_path = path.join(Config.Config().save_path, "index.html")
    if html_save_path is None or len(html_save_path) == 0:
        html_save_path = path.join(path.dirname(path.realpath(sys.argv[0])), "index.html")
    try:
        if path.exists(html_save_path) is False:
            __init_html_file(html_save_path)
        html = etree.parse(html_save_path)
        imgs_element = html.find("//imgs")

        img_element = etree.SubElement(imgs_element, "img")
        img_element.attrib["src"] = "./"+filename
        img_element.attrib["url"] = image.Url
        img_element.attrib["artist"] = image.Artist
        img_element.attrib["tag"] = __image_tag_to_str(image.Tag)
        img_element.attrib["id"] = image.Id
        img_element.attrib["posted"] = image.Posted
        img_element.attrib["size"] = image.Size
        img_element.attrib["source"] = image.Source
        img_element.attrib["rating"] = image.Rating
        img_element.attrib["score"] = image.Score
        if image.Size is not None and "x" in image.Size:
            width = image.Size.split("x")[0]
            height = image.Size.split("x")[1]
            img_element.attrib["width"] = "%d"%(int(width)/4)
            img_element.attrib["height"] = "%d"%(int(height)/4)
        else:
            img_element.attrib["width"] = "200"
            img_element.attrib["height"] = "auto"
        img_element.attrib["title"] = filename

        tags_element = html.find("//tags")
        for tag in image.Tag:
            tag_element_list = html.findall("//tags/tag")
            if tag_element_list is not None:
                for tag_element in tag_element_list:
                    if tag_element.attrib["id"] == str(tag):
                        tag_element.text = tag_element.text + "%s," % image.Id
                        break
                tag_element = etree.SubElement(tags_element, "tag")
                tag_element.attrib["id"] = str(tag)
                tag_element.text = "%s," % image.Id
            else:
                tag_element = etree.SubElement(tags_element, "tag")
                tag_element.attrib["id"] = str(tag)
                tag_element.text = "%s," % image.Id

        with open(html_save_path, 'r+', -1, 'utf-8') as file:
            file.write(etree.tostring(html).decode('utf-8'))
    except Exception as e:
        print("写入图片信息到Html文件出错[%s]" % e)



def __image_tag_to_str(tags):
    tag_str=""
    if tags is not None:
        for tag in tags:
            if tag_str == '':
                tag_str = tag
                continue
            tag_str = tag_str + "," + tag
    return tag_str

def __init_html_file(html_save_path):
    try:
        with open(html_save_path, 'w+', -1, 'utf-8') as file:
            content = ["<html>\n","<style>tags{display:none}</style>\n","<tags></tags>\n","<imgs></imgs>\n","</html>"]
            file.writelines(content)
    except Exception as e:
        print("创建html文件出错[%s]"%e)