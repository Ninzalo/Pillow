from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
import datetime
import json


def gen_image(output_path, font_path, mode, lessons_list, date, dict_file=None):
    font_size = 20
    # input_json = {
            # 'lesson_name':'Физическая культура и спорт: по выбору обучающихся (элективная дисциплина)',
            # 'type_of_lesson': 'Пр.Зан',
            # 'name': 'Карпинский А.Е.',
            # 'room': 'Спортзал 2'}
    # input_json['room'] = 'Обратите внимание, что если вы сделаете ширину линии толще c помощью width, указывая 3 точки или более через параметр xy, тогда соединительная линия между ними будет выглядеть не очень аккуратно'
    date_block = [[f'{lessons_list[0]["day_of_week"].capitalize()}'], [f'{date}'], [f'{lessons_list[0]["type_of_week"]}']]
    lessons_output_data_list = [date_block, [], [], [], [], [], []]
    max_len_line = 0
    for input_json in lessons_list:
        output_data_list = []
        input_data_list = [input_json['lesson_name'], input_json['type_of_lesson'], input_json['name'], input_json['room']]
        lesson_num = int(input_json['num'])
        for text in input_data_list:
            if len(text) > 30:
                text_list = []
                line = ''
                letter_counter = 0
                for letter_num, letter in enumerate(text):
                    letter_counter += 1
                    line += letter
                    if letter_counter > 30 and letter == ' ':
                        line = line[:-1]
                        text_list.append(line)
                        if len(line) >= max_len_line:
                            max_len_line = len(line)
                        line = ''
                        letter_counter = 0
                    if letter_counter > 35 and letter == '-':
                        line = line[:-1]
                        text_list.append(line)
                        if len(line) >= max_len_line:
                            max_len_line = len(line)
                        line = ''
                        letter_counter = 0
                    if letter_num == len(text) - 1:
                        text_list.append(line)
                        if len(line) >= max_len_line:
                            max_len_line = len(line)
                        line = ''
                        letter_counter = 0
                # for item in text_list:
                    # print(item, len(item))
            else:
                text_list = [text]
                if len(text) > max_len_line:
                    max_len_line = len(text)
            output_data_list.append(text_list)
        # lessons_output_data_list.append(output_data_list)
        lessons_output_data_list[lesson_num] = output_data_list
    letter_width = int(font_size * 6 / 10)
    letter_height = int(font_size * 72 / 60)
    gap = letter_width
    height_gap = int(font_size / 2)
    line_width = int(font_size / 20)
    rows = 0
    for output_data_list in lessons_output_data_list:
        rows_in_lesson = 0
        for lines in output_data_list:
            for line in lines:
                rows_in_lesson += 1
        if rows_in_lesson >= rows:
            rows = rows_in_lesson

    start_height = 0
    start_width = 0

    # gen image
    font = ImageFont.truetype(font=f'{font_path}\\mono.ttf', size=font_size)
    image_width = 0
    for output_data_list in lessons_output_data_list:
        max_len_line = 0
        for text_list in output_data_list:
            for text in text_list:
                if len(text) >= max_len_line:
                    max_len_line = len(text)
        image_width += start_width + gap + max_len_line * letter_width + gap
    if mode == 'night':
        fill_color = 'white'
        image = Image.new('RGB', 
                            (
                                image_width + 5,
                                start_height + letter_height * rows + height_gap + 5
                                ), 
                            (0, 0, 0))
    else:
        fill_color = 'black'
        image = Image.new('RGB', 
                            (
                                image_width + 5,
                                start_height + letter_height * rows + height_gap + 5
                                ), 
                            (255, 255, 255))
    # draw text
    idraw = ImageDraw.Draw(image)
    # print(lessons_output_data_list)
    for output_data_list in lessons_output_data_list:
        max_len_line = 0
        for text_list in output_data_list:
            for text in text_list:
                if len(text) >= max_len_line:
                    max_len_line = len(text)
        height = start_height
        for text_list in output_data_list:
            for iteration in text_list:
                idraw.text((start_width + gap, height), iteration, font=font, fill=fill_color)
                height += letter_height
        # vertical line
        idraw.line(xy=(
                        (start_width + gap + max_len_line * letter_width + gap, start_height), 
                        (start_width + gap + max_len_line * letter_width + gap, start_height + letter_height * rows + height_gap)), 
                    fill=fill_color, 
                    width=line_width)
        # horizontal line
        idraw.line(xy=(
                        (start_width, start_height + letter_height * rows + height_gap), 
                        (start_width + gap + max_len_line * letter_width + gap, start_height + letter_height * rows + height_gap)), 
                    fill=fill_color, 
                    width=line_width)
        start_width = start_width + gap + max_len_line * letter_width + gap
    image.save(output_path)


def file_input(file_path, date, subgroup):
    with open(file_path, 'r') as file:
        schedule_data = json.load(file)
    lessons = []
    for card in schedule_data:
        if card['date'] == date:
            for lesson in card['lessons']:
                if lesson['subgroup'] == subgroup or lesson['subgroup'] == '':
                    lessons.append(lesson)
    return lessons


# def file_input(file_path, days, subgroup):
    # with open(file_path, 'r') as file:
        # schedule_data = json.load(file)
    # cards = []
    # for card in schedule_data:
        # for day in days:
            # if card['date'] == day:
                # write_data = {}
                # write_data['date'] = card['date']
                # write_data['lessons'] = []
                # for lesson in card['lessons']:
                    # if lesson['subgroup'] == subgroup or lesson['subgroup'] == '':
                        # write_data['lessons'].append(lesson)
                # cards.append(write_data)
    # return cards


def main():
    group = 'АКБ 2-1'
    subgroup = '1'

    delta = 0
    today_date = datetime.datetime.today() + datetime.timedelta(days=delta * 7)
    today_date = today_date.strftime('%Y-%m-%d') 
    today_date = datetime.datetime.strptime(today_date, '%Y-%m-%d')
    today_num = today_date.weekday()
    days = []
    days = [(today_date - datetime.timedelta(days=delta)).strftime('%Y-%m-%d') for delta in reversed(range(0, today_num + 1))] 
    days += ([(today_date + datetime.timedelta(days=delta)).strftime('%Y-%m-%d') for delta in range(1, 7 - today_num)])
    # dates = []
    # for date in days:
        # date = date.split('-')
        # year = int(date[0])
        # month = int(date[1])
        # day = int(date[2])
        # date = f'{year}-{month}-{day}'
        # dates.append(date)

    # print(dates)

    # data = file_input(file_path=f'{os.getcwd()}\\Files\\schedule_{group}.json', days=dates, subgroup=subgroup)
    # for item in data:
        # # print(item)
        # print(item['date'])
        # for i in item['lessons']:
            # print(i['name'], i['type_of_lesson'])
    
    for date in days:
        try:
            date = date.split('-')
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            date = f'{year}-{month}-{day}'
            lessons = file_input(file_path=f'{os.getcwd()}\\Files\\schedule_{group}.json', date=date, subgroup=subgroup)

            modes = ['day', 'night']
            for mode in modes:
                if mode != 'night' and mode != 'day':
                    return print('Mode error')
                if not os.path.exists(f'{os.getcwd()}\\Files\\{mode}'):
                    os.mkdir(f'{os.getcwd()}\\Files\\{mode}')
                output_path = f'{os.getcwd()}\\Files\\{mode}\\week_{group}_{subgroup}_{date}.jpg' 
                font_path = f'{os.getcwd()}\\Fonts'
                gen_image(
                            output_path=output_path, 
                            font_path=font_path,
                            mode=mode,
                            lessons_list=lessons,
                            date=date,
                            )
        except:
            pass


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - start_time)
