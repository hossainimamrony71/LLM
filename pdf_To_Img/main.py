from pdf2image import convert_from_path


pdf_path = '/content/abc.pdf'


output_folder = '/content/output_images'
# !mkdir -p {output_folder}


images = convert_from_path(pdf_path)


for i, image in enumerate(images):
  image.save(f'{output_folder}/page_{i+1}.jpg', 'JPEG')

print(f'PDF converted to images and saved to "{output_folder}" folder.')