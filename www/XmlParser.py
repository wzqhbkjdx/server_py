#!/usr/bin/env python
# coding=utf-8

from xml.etree.ElementTree import ElementTree,Element
import os

def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def write_xml(tree, out_path):
    tree.write(out_path, encoding='utf-8', xml_declaration=True)

def if_match(node,kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True

def find_nodes(tree, path):
    return tree.findall(path)

def get_node_by_keyvalue(nodelist, kv_map):
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes

def change_node_properties(nodelist, kv_map, is_delete=False):
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del(node.attrib[key])
            else:
                node.set(key, kv_map.get(key))

def change_node_text(nodelist, text, is_add=False, is_delete=False):
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text

def create_node(tag, property_map, content):
    element = Element(tag, property_map)
    element.text = content
    return element


def add_child_node(nodelist, element):
    for node in nodelist:
        node.append(element)

def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)




if __name__ == '__main__':
    tree = read_xml('templates/iphone_dev_model.xml')
    
    nodes = find_nodes(tree, 'dict')
    a = create_node('key',{}, 'BLUEADDRESS')
    add_child_node(nodes, a)
    b = create_node('string', {}, '15:fe:08:d8:b5:f3')
    add_child_node(nodes, b)
    write_xml(tree, './out.xml')

    with open('./out.xml') as file:
        data = file.read()

    os.remove('./out.xml')

    print("$$" + data)
