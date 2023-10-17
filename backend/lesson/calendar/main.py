import combine
import generate_calendar
import generate_image


if __name__ == '__main__':
    year = int(input("Year: "))
    month = int(input("Month: "))
    prompt = input("Image prompt: ")
    
    image_path = generate_image.generate(prompt)
    calendar_path = generate_calendar.generate(year, month)
    
    combine.generate(image_path, calendar_path)
