import os
import subprocess

def compile_scss_to_css(scss_dir, css_dir):
    if not os.path.isdir(scss_dir):
        print(f"❌ SCSS directory '{scss_dir}' not found.")
        return
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)

    for filename in os.listdir(scss_dir):
        if filename.endswith(".scss"):
            input_path = os.path.join(scss_dir, filename)
            output_filename = filename.replace(".scss", ".css")
            output_path = os.path.join(css_dir, output_filename)

            try:
                print(f"🔄 Compiling {filename} → {output_filename}")
                subprocess.run(["sass", input_path, output_path], check=True)
            except subprocess.CalledProcessError:
                print(f"❌ Failed to compile {filename}")

    print("✅ All SCSS files compiled to CSS.\nSay thanks for Kakharov.\nhttps://taplink.cc/qaxxorovc")