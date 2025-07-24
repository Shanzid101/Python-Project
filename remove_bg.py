# Required libraries
# pip install rembg pillow

from rembg import remove
from PIL import Image
import os
import io

def remove_background(input_path, output_path, target_width=None, target_height=None):
    """
    remove the background from an image and resize it to specified dimensions.
    """
    try:
        
        with open(input_path, "rb") as f:
            input_image_bytes = f.read()

        output_image_bytes = remove(input_image_bytes)

        output_image = Image.open(io.BytesIO(output_image_bytes))

        
        if target_width and target_height:
            
            output_image = output_image.resize((target_width, target_height), Image.LANCZOS)
            print(f"🖼️ Image resized to {target_width}x{target_height} pixels.")

        
        output_image.save(output_path, format="PNG") # if you want to save as PNG or any other format.change as needed(PNG, JPEG, etc.)

        return output_path
    except FileNotFoundError:
        print(f"Error: input file '{input_path}' not found.")
        return None
    except Exception as e:
        print(f"error: {e}")
        return None

def main():
    input_file = "image.jpeg"  
    output_png = "image_no_bg_hd.png"

    # Set target dimensions for HD quality(1536x1080, which is 16:9 aspect ratio.or any other dimensions you prefer)
    hd_width = 1536
    hd_height = 1080

    print("\n remove background and save...")
    
    result_path = remove_background(input_file, output_png, target_width=hd_width, target_height=hd_height)

    if result_path:
        print(f" removed background and saved: {result_path}")
    else:
        print(" Failed to remove background or save the image.")

if __name__ == "__main__":
    main()
