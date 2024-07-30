from PIL import Image
import io
import os

def generate_thumbnail(input_stream, max_dimension=1170):
    # Open an image from the input stream
    img = Image.open(input_stream)
    
    # Calculate the aspect ratio
    aspect_ratio = min(max_dimension / img.width, max_dimension / img.height)
    
    # Calculate the new size while maintaining the aspect ratio
    new_size = (int(img.width * aspect_ratio), int(img.height * aspect_ratio))
    
    # Resize the image
    img.thumbnail(new_size, Image.Resampling.LANCZOS)
    
    # Create an output stream
    output_stream = io.BytesIO()
    
    # Save the thumbnail to the output stream with optimization
    if img.format == 'JPEG':
        img.save(output_stream, format='JPEG', optimize=True, quality=85)
    elif img.format == 'PNG':
        img.save(output_stream, format='PNG', optimize=True, compress_level=9)
    else:
        img.save(output_stream, format=img.format)
    
    # Seek to the beginning of the output stream
    output_stream.seek(0)
    
    return output_stream

def process_image_file(input_path):
    # Read the image file into a BytesIO stream
    with open(input_path, 'rb') as input_file:
        input_stream = io.BytesIO(input_file.read())
    
    # Generate the thumbnail and get the output stream
    output_stream = generate_thumbnail(input_stream)
    
    # Get the file name and extension
    base_name, ext = os.path.splitext(input_path)
    output_path = f"{base_name}_thumbnail{ext}"
    
    # Save the output stream to a file with the new name
    with open(output_path, 'wb') as output_file:
        output_file.write(output_stream.getvalue())
    
    print(f"Thumbnail saved to {output_path}")

# Call the example function with an input image file
process_image_file(r'D:\OneDrive\Azure_BHM\tennis\595\image1_20240718042444.png')
