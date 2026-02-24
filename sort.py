import pygame as pg
import random
import time
import numpy as np

pg.init()
pg.mixer.init(frequency=44100, size=-16, channels=1)

favi = pg.image.load("faivcon.png")
pg.display.set_icon(favi)

WIDTH,HEIGHT = 1200,700
screen = pg.display.set_mode((WIDTH,HEIGHT))

black = (0,0,0)
green = (0,255,0)
light_green = (150, 255, 150)
red = (255,0,0)
white = (255,255,255)

N_Elements = 200
array = [random.randint(50,HEIGHT-50) for _ in range (N_Elements)]
Bar_Width = WIDTH // N_Elements

sort_sound = pg.mixer.Sound("laser.wav")

text_font = pg.font.Font("Robotic Harlequin.otf",35)

def draw_txt(text,font,txt_color,x,y):
    img = font.render(text, True, txt_color)
    screen.blit(img, (x,y))

indent = 20

last_hovered = None
def main_menu():
    global last_hovered
    pg.display.set_caption("Sorting Algorimths Visualization")
    screen.fill(black)
    y = 25
    button_data = [
        ("Bubble Sort", """   Repeatedly swaps 
adjacent elements if 
        they are in the 
        wrong order.
------------------
    time complexity
         
              O(N^2)
""", y),
        ("Selection Sort", """    Finds the smallest
    element in the
    unsorted part and 
    places it 
    at the beginning.
------------------
    time complexity
         
              O(N^2)
""", y+100),
        ("Quick Sort","""Divides the array around
a pivot and recursively
sorts the partitions.
------------------
    time complexity
         
              O(N^2)
""", y+200),
        ("Insertion Sort","""    Builds the sorted
    list one element at
    a time by inserting
    into the correct 
    position.
------------------
    time complexity
         
              O(N^2)
""", y+300),
        ("Heap Sort", """    Builds a heap 
    and repeatedly
    extracts the 
    maximum / minimum
    to sort the array.
------------------
    time complexity
         
          O(n log n)
""", y+400),
        ("Merge Sort", """Recursively splits
the array into halves 
and merges them back in
sorted order.
------------------
    time complexity
         
          O(n log n)
""", y+500),
        ("Bitonic Sort", """builds a sequence that
rises then falls, and
through repeated compare 
and swap steps merges
it into sorted order.
------------------
    time complexity
         
        O(n*(log n)^2) 

""", y+600),
    ]

    buttons = {}
    mouse_pos = pg.mouse.get_pos()

    for name,desc,ypos in button_data:
        color = green
        font_size = 35
        rect_area = pg.Rect(indent, ypos, 300, 50)
        if rect_area.collidepoint(mouse_pos):
            if last_hovered != name:
                hover = pg.mixer.Sound("hover.wav")
                hover.play()
            last_hovered = name
            color = light_green
            font_size = 40
            desc_img = text_font.render(desc, True, white)
            screen.blit(desc_img, (500, 150))
        else:
            if last_hovered == name:
                last_hovered = None

            
        hover_font = pg.font.Font("Robotic Harlequin.otf", font_size)
        img = hover_font.render(name, True, color)
        rect = img.get_rect(topleft=(indent, ypos))
        screen.blit(img,rect)
        buttons[name] = rect

    return buttons



def draw_array(highlight_indices=[]):
    screen.fill(black)
    for i,val in enumerate(array):
        x = i * Bar_Width
        color = green
        if i in highlight_indices:
            color = white
        pg.draw.rect(screen,color,(x,HEIGHT-val,Bar_Width,val))
    pg.display.update()
        

def Bubble(array):
    pg.display.set_caption("Bubble Sort Visualization")
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
                    running = False
                    return array
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
                        running = False
                        return array
            draw_array(highlight_indices=[j, j+1])
            pg.time.delay(1)

            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                sort_sound.play()

    array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
    return array


def Selection(array):
    pg.display.set_caption("Selection Sort Visualization")
    lin = range(0,len(array)-1)
    for i in lin:
        min = i
        for j in range (i+1,len(array)):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
                    running = False
                    return array
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
                        running = False
                        return array
            if array[j] < array[min]:
                min = j
        if min != i:
            draw_array(highlight_indices=[i,min])
            array[min], array[i] = array[i],array[min]
            sort_sound.play()
            pg.time.wait(75)
        
    array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
    return array

def Quick(array, low = 0, high = None):
    pg.display.set_caption("Quick Sort Visualization")
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            sorting = False
            return array

    if high is None:
        high = len(array)-1
    if low < high:
        pi = partition(array, low, high)
        Quick(array, low, pi-1)
        Quick(array,pi+1, high)
    return array

def partition(array, low, high):
    pivot = array[high]
    i = low - 1

    for j in range (low, high):
        if array[j] <= pivot:
            i+=1
            array[i], array[j] = array[j], array[i]
        draw_array(highlight_indices=[j, high])
        sort_sound.play()
        pg.time.wait(5)

    array[i+1], array[high] = array[high], array[i+1]
    draw_array(highlight_indices=[i + 1, high])
    pg.time.wait(5)

    return i+1

def Insertion(array):
    pg.display.set_caption("Insertion Sort Visualization")
    for i in range(1, len(array)):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                array[:] = [random.randint (50, HEIGHT-50) for _ in range (N_Elements)]
                running  = False
                return array
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    array[:] = [random.randint (50, HEIGHT-50) for _ in range (N_Elements)]
                    running  = False
                    return array
        key = array[i]
        j = i-1
        while j >= 0 and array[j] > key:
            array[j+1] = array[j]
            j -=1
            draw_array(highlight_indices=[j+1, i])
            sort_sound.play()
            pg.time.delay(1)
        array[j+1] = key
        draw_array(highlight_indices=[j+1, i])
        pg.time.delay(1)
    
    return array


def merge_sort(array, low=0, high=None):
    pg.display.set_caption("Merge Sort Visualization")
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            sorting = False
            return array
    if high is None:
        high = len(array) - 1
    if low < high:
        mid = (low + high) // 2
        merge_sort(array, low, mid)
        merge_sort(array, mid + 1, high)
        merge(array, low, mid, high)
    return array

def merge(array, low, mid, high):
    left = array[low:mid+1]
    right = array[mid+1:high+1]
    i = j = 0
    k = low
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            array[k] = left[i]
            i += 1
        else:
            array[k] = right[j]
            j += 1
        draw_array(highlight_indices=[k])
        sort_sound.play()
        pg.time.wait(1)
        k += 1
    while i < len(left):
        array[k] = left[i]
        i += 1
        draw_array(highlight_indices=[k])
        pg.time.wait(1)
        k += 1
    while j < len(right):
        array[k] = right[j]
        j += 1
        draw_array(highlight_indices=[k])
        pg.time.wait(1)
        k += 1
    return array

def heapify(array, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and array[left] > array[largest]:
        largest = left
    if right < n and array[right] > array[largest]:
        largest = right

    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        draw_array(highlight_indices=[i, largest])
        sort_sound.play()
        pg.time.wait(1)
        heapify(array, n, largest)

def heap_sort(array):
    pg.display.set_caption("Heap Sort Visualization")
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            sorting = False
            return array
    n = len(array)

    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i)

    for i in range(n - 1, 0, -1):
        
        array[0], array[i] = array[i], array[0]
        draw_array(highlight_indices=[0, i])
        sort_sound.play()
        pg.time.wait(1)
        heapify(array, i, 0)

    return array

def compare_and_swap(array, i, j, direction):
    if (direction == 1 and array[i] > array[j]) or (direction == 0 and array[i] < array[j]):
        array[i], array[j] = array[j], array[i]
        draw_array(highlight_indices=[i, j])
        sort_sound.play()
        pg.time.wait(5)

def bitonic_merge(array, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            compare_and_swap(array, i, i + k, direction)
        bitonic_merge(array, low, k, direction)
        bitonic_merge(array, low + k, k, direction)

def bitonic_sort(array, low=0, cnt=None, direction=1):
    pg.display.set_caption("Bitonic Sort Visualization")
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            sorting = False
            return array
    
    if cnt is None:
        cnt = len(array)
    if cnt > 1:
        k = cnt // 2
        bitonic_sort(array, low, k, 1)
        bitonic_sort(array, low + k, k, 0)
        bitonic_merge(array, low, cnt, direction)
    return array

running = True
sorting = False
while running:
    buttons = main_menu()
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos

            for name, rect in buttons.items():
                if rect.collidepoint(pos):
                    click = pg.mixer.Sound("click.wav")
                    click.play()
                    if(name == "Bitonic Sort"):
                        sorting = True
                        bitonic_sort(array)
                        array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
                        sorting = False
                    elif(name == "Bubble Sort"):
                        Bubble(array)
                    elif(name == "Selection Sort"):
                        Selection(array)
                    elif(name == "Quick Sort"):
                        sorting = True
                        Quick(array)
                        array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
                        sorting = False
                    elif(name == "Insertion Sort"):
                        Insertion(array)
                    elif(name == "Merge Sort"):
                        sorting = True
                        merge_sort(array)
                        array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
                        sorting = False
                    elif(name == "Heap Sort"):
                        sorting = True
                        heap_sort(array)
                        array[:] = [random.randint(50, HEIGHT-50) for _ in range(N_Elements)]
                        sorting = False

                        
pg.quit()
