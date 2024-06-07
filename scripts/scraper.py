import os
import re


def parse_svg_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".svg"):
                svg_path = os.path.join(root, file)
                with open(svg_path, "r") as svg_file:
                    svg_content = svg_file.read()

                    # Find the first <svg> tag
                    first_svg_match = re.search(r"<svg[^>]*>", svg_content)
                    if first_svg_match:
                        first_svg_tag = first_svg_match.group(0)
                        class_attr = f"class={{class}}"
                        if "class=" not in first_svg_tag:
                            # If class attribute not present in the first <svg> tag, add it
                            svg_content = svg_content.replace(
                                first_svg_tag, f"{first_svg_tag[:-1]} {class_attr}>", 1
                            )
                        else:
                            # If class attribute already present, insert 'class={{class}}' after it
                            svg_content = svg_content.replace(
                                first_svg_tag, f"{first_svg_tag[:-1]} {class_attr} ", 1
                            )
                    package_name = "icons"
                    class_name = os.path.splitext(file)[0].capitalize()
                    templ_content = f"""package {package_name}
                        templ {class_name}(class string) {{
                        {svg_content}
                        }}"""

                    target_dir = os.path.join("./scraped/solid")
                    os.makedirs(target_dir, exist_ok=True)

                    templ_path = os.path.join(target_dir, f"{class_name}.templ")
                    with open(templ_path, "w") as templ_file:
                        templ_file.write(templ_content)


# Example usage:
directory_path = "../src/solid"
parse_svg_files(directory_path)
