#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""XML parsing utility"""

import xml.etree.ElementTree as ET
from typing import Dict, Any


class XmlParser:
    """XML解析工具类 - 简化版"""
    
    NS = {'evt': 'http://schemas.microsoft.com/win/2004/08/events/event'}
    
    @classmethod
    def extract_basic_fields(cls, xml_content: str) -> Dict[str, Any]:
        """从XML中提取基础字段（简化版）"""
        fields = {}
        
        try:
            root = ET.fromstring(xml_content)
            
            # 基础字段
            fields['EventID'] = cls._extract_text(root, './/EventID')
            fields['Level'] = cls._extract_text(root, './/Level')
            fields['TimeCreated'] = cls._extract_attr(root, './/TimeCreated', 'SystemTime')
            fields['Computer'] = cls._extract_text(root, './/Computer')
            fields['Channel'] = cls._extract_text(root, './/Channel')
            fields['Provider_Name'] = cls._extract_attr(root, './/Provider', 'Name')
                        
        except Exception as e:
            pass
            
        return fields
    
    @classmethod
    def _extract_text(cls, root: ET.Element, xpath: str) -> str:
        """提取元素文本"""
        try:
            element = root.find(xpath)
            if element is not None and element.text:
                return element.text.strip()
            
            namespaced_xpath = xpath.replace('.//', './/{http://schemas.microsoft.com/win/2004/08/events/event}')
            element = root.find(namespaced_xpath)
            if element is not None and element.text:
                return element.text.strip()
            
            return ''
        except:
            return ''
    
    @classmethod
    def _extract_attr(cls, root: ET.Element, xpath: str, attr_name: str) -> str:
        """提取元素属性"""
        try:
            element = root.find(xpath)
            if element is not None:
                return element.get(attr_name, '')
            
            namespaced_xpath = xpath.replace('.//', './/{http://schemas.microsoft.com/win/2004/08/events/event}')
            element = root.find(namespaced_xpath)
            if element is not None:
                return element.get(attr_name, '')
            
            return ''
        except:
            return ''
