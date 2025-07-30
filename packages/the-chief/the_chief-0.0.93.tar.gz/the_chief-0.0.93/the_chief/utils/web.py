from bs4 import BeautifulSoup, Comment

def get_simplified_html(html: str, selector=None) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    # 如果指定了selector，则只提取该元素的内容
    if selector:
        element = soup.select_one(selector)
        if element:
            soup = BeautifulSoup(str(element), 'html.parser')
        else:
            return f"element not found: {selector}"

    # 定义需要移除的标签
    tags_to_remove = ['script', 'style', 'noscript', 'meta', 'link']
    for tag in tags_to_remove:
        for element in soup(tag):
            element.decompose()

    # 移除注释
    for element in soup.find_all(string=lambda text: isinstance(text, Comment)):
        element.extract()

    # 定义需要保留的交互属性
    INTERACTIVE_ATTRIBUTES = {
        'a': ['href', 'onclick'],
        'button': ['onclick'],
        'img': ['src', 'onload'],
        'form': ['action', 'onsubmit'],
        'input': ['type', 'onclick', 'onchange'],
        '*': ['onclick', 'onload', 'onchange', 'onsubmit', 'onmouseover']
    }

    # 遍历所有标签，保留交互属性并移除其他属性
    for element in soup.find_all(True):
        tag_name = element.name
        allowed_attrs = INTERACTIVE_ATTRIBUTES.get(tag_name, []) + INTERACTIVE_ATTRIBUTES['*']
        attrs = list(element.attrs.keys())
        for attr in attrs:
            if attr not in allowed_attrs:
                del element[attr]

        # 如果是<img>标签，检查src是否为Base64
        if tag_name == 'img' and 'src' in element.attrs and element['src'].startswith('data:'):
            del element['src']

        # 处理文本内容，超过1000字符则截取
        if element.string and len(element.string) > 1000:
            element.string = element.string[:1000] + '...'

    # 移除标签之间的多余空白
    for element in soup.find_all(True):
        if not element.get_text(strip=True):
            element.string = ''

    return str(soup)