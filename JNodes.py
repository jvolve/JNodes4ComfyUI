from pathlib import Path
import re

# STRINGS

class J_StringContains:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", { "multiline": False, "default": "", "forceInput": True }),
                "substring": ("STRING", { "multiline": False, "default": "" }),
                "success_result": ("STRING", { "multiline": False, "default": "" }),
                "default_result": ("STRING", { "multiline": False, "default": "" }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)

    FUNCTION = "string_contains"

    OUTPUT_NODE = True

    CATEGORY = "JNodes"

    def string_contains(self, input_str, substring, success_result, default_result):
        if substring.lower() in input_str.lower():
            return (success_result,)
        
        return (default_result,)

class J_StringAppend:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", { "multiline": False, "default": "", "forceInput": True }),
                "append_str": ("STRING", { "multiline": False, "default": "" }),
                "separator": ("STRING", { "multiline": False, "default": "" }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)

    FUNCTION = "string_append"

    OUTPUT_NODE = True

    CATEGORY = "JNodes"

    def string_append(self, input_str, append_str, separator):
        result = input_str + separator + append_str
        
        return (result,)

class J_StringSplit:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", { "multiline": False, "default": "", "forceInput": True }),
                "split_chars": ("STRING", { "multiline": False, "default": "," }),
                "trim_whitespace": ("BOOLEAN", { "default": True }),
                "other_trim_chars": ("STRING", { "multiline": False, "default": "" }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string_list",)

    FUNCTION = "string_split"

    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "JNodes"

    def string_split(self, input_str, split_chars, trim_whitespace, other_trim_chars):
        delimiters = list(set(split_chars))
        split_pattern = '|'.join(map(re.escape, delimiters))
        
        result = re.split(split_pattern, input_str)
        
        trim_chars = "" + other_trim_chars
        if trim_whitespace:
            trim_chars += " "
        
        unique_trim_chars = "".join(set(trim_chars))
        
        for i, s in enumerate(result):
            result[i] = s.strip(unique_trim_chars)
            # print(f"J_StringSplit.string_split(): {result[i]}")
        
        return (result,)

class J_StringSelect:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_list": ("STRING", { "forceInput": True }),
                "select": ("INT", { "default": 0, "min": 0, "step": 1, "display": "number" }),
            },
        }
    
    INPUT_IS_LIST = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected",)

    FUNCTION = "string_select"

    OUTPUT_NODE = True

    CATEGORY = "JNodes"

    def string_select(self, input_list, select):
        selectIndex = select[0]
        if len(input_list) > 0 and selectIndex < len(input_list):
            result = input_list[selectIndex]
            return (result,)
        
        return ("",)

OUTPUT_TYPE_MATCHED_STRING = "matched string"
OUTPUT_TYPE_MATCHED_GENDER = "matched gender"

class J_StringSelectByGender:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_list": ("STRING", { "forceInput": True }),
                "default_if_not_found": ("STRING", { "multiline": False, "default": "person" }),
                "output_type": ([OUTPUT_TYPE_MATCHED_STRING, OUTPUT_TYPE_MATCHED_GENDER],),
            },
        }
    
    INPUT_IS_LIST = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("match",)

    FUNCTION = "string_select"

    OUTPUT_NODE = True

    CATEGORY = "JNodes"

    def string_select(self, input_list, default_if_not_found, output_type):
        default = default_if_not_found[0]
        if len(input_list) == 0:
            return (default,)
        
        rx = re.compile(r"\b(man|woman|girl|boy)\b")
        for s in input_list:
            match = rx.search(s)
            if match:
                if (output_type[0] == OUTPUT_TYPE_MATCHED_GENDER):
                    return (match[0],)
                return (s,)
        
        return (default,)

class J_FilenameWithoutExtension:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", { "forceInput": True }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filename",)

    FUNCTION = "doit"

    OUTPUT_NODE = True

    CATEGORY = "JNodes"

    def doit(self, path:str):
        result = Path(path.strip("\" ")).stem
        
        return (result,)



NODE_CLASS_MAPPINGS = {
    "J Contains String": J_StringContains,
    "J Append String": J_StringAppend,
    "J Split String": J_StringSplit,
    "J Select String": J_StringSelect,
    "J Select String By Gender": J_StringSelectByGender,
    "J Filename Without Extension": J_FilenameWithoutExtension,
}
