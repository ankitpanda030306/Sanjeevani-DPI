with open("build_datasets.py", "r", encoding="utf-8") as f:
    code = f.read()

old_e11 = '"concept_name": "Type 2 diabetes mellitus"'
if old_e11 in code:
    idx = code.find(old_e11)
    syn_idx = code.find('"synonyms":', idx)
    end_bracket = code.find(']', syn_idx)
    code = code[:syn_idx] + '"synonyms": ["diabetes", "sugar", "high blood sugar", "polyuria", "diabetic checkup", "t2dm", "hyperglycemia"]' + code[end_bracket+1:]
    with open("build_datasets.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Updated E11.9 diabetes synonyms in build_datasets.py")
