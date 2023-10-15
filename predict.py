from ultralytics import YOLO
import cv2, os, json, shutil
from PIL import Image
import math, csv, time
import check

source = './test/28027647.jpg'

print_image_data = False
show_image = False
save_car_number = False
save_car_number_data = False


input_dir = 'C:/Users/kolya/OneDrive/Documents/MyProjects/Python/AI vagons/test_dataset/'
model1_name = 'model1.pt'
model2_name = 'model2.pt'

def calculate_control_number(wagon_number, abbreviated_wagon_number):
    # Проверяем, что номер вагона соответствует длине длину
    if len(wagon_number) != 8:
        return None  # Если длина не соответствует ожидаемой, возвращаем None

    weight_range = [2, 1, 2, 1, 2, 1, 2]

    # Проверяем, что сокращённый номер вагона и весовой ряд имеют одинаковую длину
    if len(abbreviated_wagon_number) != len(weight_range):
        return None  # Возвращаем None в случае ошибки

    # Вычисляем поразрядные произведения и суммируем их
    multiplication = [
        int(abbreviated_wagon_number[i]) * weight_range[i]
        for i in range(len(abbreviated_wagon_number))
    ]
    total_sum = sum([mult // 10 + mult % 10 for mult in multiplication])

    # Вычисляем контрольное число
    counted_control_number = (10 - (total_sum % 10)) % 10

    return counted_control_number

def check_number(wagon_number: str):
    if len(wagon_number) != 8:
        return 0
    abbreviated_wagon_number = wagon_number[:7]  # Первые 7 чисел
    control_number = int(wagon_number[7])  # Последнее восьмое число

    counted_control_number = calculate_control_number(wagon_number, abbreviated_wagon_number)

    if counted_control_number is not None:
        if counted_control_number == control_number:
            return 1
        else:
            return 0
    else:
        return 0

def create_required_dirs(dir_for_result):
    if not os.path.isdir(dir_for_result):
        os.makedirs(dir_for_result)
    if not os.path.isdir(dir_for_result + '/images'):
        os.makedirs(dir_for_result + '/images')
    if not os.path.isdir(dir_for_result + '/labels'):
        os.makedirs(dir_for_result + '/labels')

def save_correct_result(full_path, filename, symbols, width, height):
    dir_for_result = "./new_datas"
    create_required_dirs(dir_for_result)
    with open(dir_for_result + "/labels/" + filename + '.txt', 'w') as savefile:
        for symbol in symbols:

            box = symbol['box']

            center_x = (box['x1'] + box['x2']) / 2 / width
            center_y = (box['y1'] + box['y2']) / 2 / height
            new_width = math.fabs(box['x2'] - box['x1']) / width
            new_height = math.fabs(box['y2'] - box['y1']) / height

            savefile.write(str(symbol['class']) + ' ' + str(center_x) + ' ' + str(center_y) + ' ' + str(new_width) + ' ' + str(new_height) + '\n')

def get_car_number(img, dir, filename, width, height):
    full_path = dir + filename
    model = YOLO(model2_name)
    response_result = model(img)
    result = []
    for item in response_result:
        js = json.loads(item.tojson())
        if not js == []:
            js.sort(key = lambda i: i['box']['x1'])
            number = ""
            symbol_boxes = []
            for symbol in js:
                number += str(symbol['class'])
                symbol_boxes.append(symbol['class'])
                symbol_boxes.append(symbol['confidence'])

            if save_car_number_data and (number == filename.split('.')[0].replace('_','')):
                save_correct_result(full_path, filename.split('.')[0], js, width, height)
            
            data = []
            data.append(number)
            data.append(symbol_boxes)
            result.append(data)
    return result

def cut_image(dir, filename, x1, y1, x2, y2):
    full_path = dir + filename
    img = cv2.imread(full_path, 1)
    crop_img = img[int(y1):int(y2), int(x1):int(x2)]
    if not os.path.isdir('./car_numbers'):
        os.makedirs('./car_numbers')
    if save_car_number:
        cv2.imwrite('./car_numbers/' + full_path.split('/')[-1], crop_img)

    if show_image:
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 5)
        cv2.imshow('image', crop_img)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
    
    return crop_img

def find_car_number(dir, filename):
    model = YOLO(model1_name)
    response_results = model(dir + filename)
    result = []
    for i in response_results:
        js = json.loads(i.tojson())
        if not js == []:
            data = []
            img = cut_image(dir, filename, js[0]['box']['x1'], js[0]['box']['y1'], js[0]['box']['x2'], js[0]['box']['y2'])
            data.append(img)
            box_number = {'x1': js[0]['box']['x1'], 'y1': js[0]['box']['y1'], 'x2': js[0]['box']['x2'], 'y2': js[0]['box']['y2']}
            data.append(box_number)
            data.append(js[0]['confidence'])
            result.append(data)
    return result


def main():
    f = open('./result.csv', 'w')
    writer = csv.writer(f)
    header = ['filename', 'type', 'number', 'is_correct']
    writer.writerow(header)
    for filename in os.listdir(input_dir):
        row = ['dataset/' + filename, '0', '0', '0']
        start = time.time() * 1000
        result1 = find_car_number(input_dir, filename)
        time1 = time.time() * 1000
        for item in result1:
            if item != []:
                row[1] = '1'
                result2 = get_car_number(item[0], input_dir, filename, math.fabs(item[1]['x1'] - item[1]['y1']), math.fabs(item[1]['x2'] - item[1]['y2']))
                time2 = time.time() * 1000
                for i in result2:
                    row[2] = i[0]
                    if check_number(i[0]):
                        row[3] = '1'
                    print('\n')
                    print(f'Input: {filename}')
                    print(f'Output: {i[0]}')
                    print(f'Time1: {(time1 - start)}')
                    print(f'Time2: {(time2 - time1)}')
                    print('\n')
        writer.writerow(row)

if __name__ == '__main__':
    main()