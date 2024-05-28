from re import compile
from collections import OrderedDict

# compiled regex strings

remove_nonprompts_regex = compile(r"[^a-zA-Z()\[\]{}]*")
remove_nonweighters_regex = compile(r"[()\[\]{}]*")
remove_inside_regex = compile(r"[^()\[\]{}]*")

find_empty_parantheses_regex = compile(r"\(\s*\)")

remove_multiwhitespaces_regex = compile(r"\s+")
remove_nonpromptcommas_regex = compile(r"(,\s){2,}")
remove_scalarweights_regex = compile(r",\s*:[0-9]*\.?[0-9]+")
remove_emptyprompts_regex = compile(r",\s+[()\[\]{}]+\s*,")
remove_danglingparantheses_regex = compile(r"\s+[()]*\s+[^a-zA-Z0-9]+")


def GetUniqueList(sequence: list) -> list:
    seen = set()
    return [x for x in sequence if not (x.strip() in seen or seen.add(x.strip()))]


def remove_exact_keywords(line: str) -> list[str]:
    # remove exact prompts
    prompts = GetUniqueList(line.split(","))

    pure_prompts = OrderedDict()  # order matters, it contains prompts' original forms
    extracted_pure_prompts = {}  # order isn't important, it contains prompt keywords

    # remove exact keyword
    for prompt in prompts:
        tempPrompt = remove_nonprompts_regex.sub(
            "", prompt
        ).lstrip()  # from -> ((masterpiece:1.2)) | to -> ((masterpiece))

        if tempPrompt == "":
            continue

        tempPrompt = remove_nonweighters_regex.sub(
            "", tempPrompt
        )  # from -> ((masterpiece)) | to -> masterpiece

        if tempPrompt in extracted_pure_prompts:
            tempPrompt = remove_inside_regex.sub(
                "", prompt
            )  # from -> ((masterpiece:1.2)) | to -> (())

            if (
                len(find_empty_parantheses_regex.findall(tempPrompt))
                > 0  # find () count
                or tempPrompt == ""
            ):
                # check balanced parantheses
                inner_parant_count = tempPrompt.count("(")
                outer_parant_count = tempPrompt.count(")")

                if inner_parant_count == outer_parant_count:
                    continue

                lowest_count = min(inner_parant_count, outer_parant_count)

                # remove balanced parantheses
                # because it is going to be appended to previous string
                for _ in range(lowest_count):
                    tempPrompt = tempPrompt.replace("()", "")

            pure_prompts[tempPrompt] = True
            continue

        if tempPrompt == "":
            tempPrompt = remove_nonprompts_regex.sub("", prompt).lstrip()
            pure_prompts[tempPrompt] = True
        else:
            extracted_pure_prompts[tempPrompt] = True
            pure_prompts[prompt] = True

    return pure_prompts.keys()


def Preprocess(line: str) -> str:

    temp_line = line.encode("ascii", "xmlcharrefreplace").decode()
    temp_line = temp_line.encode(errors="xmlcharrefreplace").decode()

    temp_line = temp_line.replace("\xa0", " ")
    temp_line = temp_line.replace("\n", ", ")
    temp_line = remove_multiwhitespaces_regex.sub(
        " ", temp_line
    )  # from -> ,       ,  , (     prompt) | to -> , , , (prompt)

    temp_line = remove_nonpromptcommas_regex.sub(
        ", ", temp_line
    )  # from -> , , , , | to -> ,

    temp_line = remove_scalarweights_regex.sub(
        "", temp_line
    )  # from -> , 0.6 | to -> *empty string*

    temp_line = ", ".join(remove_exact_keywords(temp_line))

    temp_line = remove_multiwhitespaces_regex.sub(
        " ", temp_line
    )  # from -> ,       ,  , (       prompt) | to -> , , , (prompt)

    temp_line = remove_nonpromptcommas_regex.sub(
        ", ", temp_line
    )  # from -> , , , , | to -> ,

    # fixing the artifacts
    replace_dict = {
        "(,": "(",
        "[,": "[",
        "{,": "{",
        ", )": ")",
        ", ]": "]",
        ", }": "}",
    }

    for old_str, new_str in replace_dict.items():
        temp_line = temp_line.replace(old_str, new_str)

    temp_line = remove_emptyprompts_regex.sub(
        ",", temp_line
    )  # from -> , (((, | to -> ,

    temp_line = remove_danglingparantheses_regex.sub(
        " ", temp_line
    )  # from -> (( ((prompt)) | to -> ((prompt))

    return temp_line
