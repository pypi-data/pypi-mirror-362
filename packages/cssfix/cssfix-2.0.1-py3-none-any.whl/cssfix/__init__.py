import re

class css(str):
    def __new__(cls, css_text):
        cleaned_css = cls.remove_comments(css_text)
        rules = cls.parse_rules(cleaned_css)
        merged = cls.merge_rules(rules)
        optimized = ''.join(f'{selector}{{{cls.minify_properties(props)}}}' for selector, props in merged.items())
        return str.__new__(cls, optimized)

    @staticmethod
    def remove_comments(css):
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        css = css.replace("\n", "")
        return css

    @staticmethod
    def parse_rules(css):
        pattern = re.compile(r'([^{]+)\{([^}]+)\}')
        rules = pattern.findall(css)
        return [(selector.strip(), properties.strip()) for selector, properties in rules]

    @staticmethod
    def merge_properties(props1, props2):
        props_dict = {}
        for prop in props1.split(';'):
            if ':' in prop:
                k, v = prop.split(':', 1)
                props_dict[k.strip()] = v.strip()
        for prop in props2.split(';'):
            if ':' in prop:
                k, v = prop.split(':', 1)
                props_dict[k.strip()] = v.strip()
        return '; '.join(f'{k}: {v}' for k, v in props_dict.items() if k) + ';'

    @classmethod
    def merge_rules(cls, rules):
        merged = {}
        for selector, props in rules:
            if not props.strip():
                continue
            selectors = [s.strip() for s in selector.split(',')]
            for sel in selectors:
                if sel in merged:
                    merged[sel] = cls.merge_properties(merged[sel], props)
                else:
                    merged[sel] = props
        return merged

    @staticmethod
    def minify_properties(props):
        props = props.strip().rstrip(';')
        props_list = props.split(';')
        props_dict = {}
        for p in props_list:
            if ':' not in p:
                continue
            k, v = p.split(':', 1)
            k = k.strip()
            v = v.strip()
            v = re.sub(r'\b0(px|em|rem|%)\b', '0', v)
            if re.match(r'^#([0-9a-fA-F]{6})$', v):
                hexv = v[1:]
                if hexv[0]==hexv[1]==hexv[2] and hexv[2]==hexv[3]==hexv[4]==hexv[5]:
                    v = '#' + hexv[0] + hexv[2] + hexv[4]
            if k in ['margin', 'padding']:
                parts = v.split()
                if all(p == '0' for p in parts):
                    v = '0'
            props_dict[k] = v
        data = ';'.join(f'{k}:{v}' for k, v in props_dict.items()) + ';'
        return data.replace("  ","")