#!/usr/bin/env python3
import threading
import cv2
import base64
from Queue import Queue


def extract_frames(fileName, framesQueue, maxFramesToLoad=999):
    vidcap = cv2.VideoCapture(fileName)
    success, image = vidcap.read()

    print('Frame extraction started')
    count = 0
    while success and count < maxFramesToLoad:
        success, jpgImage = cv2.imencode('.jpg', image)

        jpgAsText = base64.b64encode(jpgImage)

        #putting the extracted frames into the queue where they hold a lock
        framesQueue.enqueue(image)
        print(f'Reading frame {count} {success}')

        success, image = vidcap.read()
        count += 1

    print('Frame extraction completed')
    framesQueue.kill()


#This is a producer and also a consumer
def convert_to_grayscale(framesQueue, grayScaleQueue):
    print('Conversion to grayscale started')
    count = 0

    while framesQueue.isActive() or not framesQueue.isEmpty():
        inputFrame = framesQueue.deque()
        print(f'Converting frame {count}')

        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

        #putting grayscale frames in the queue while they hold a lock
        grayScaleQueue.enqueue(grayscaleFrame)

        count += 1

    print('Conversion to grayscale completed')
    grayScaleQueue.kill()


def display_frames(grayScaleQueue):
    count = 0

    print('Started displaying all frames')
    while grayScaleQueue.isActive() or not grayScaleQueue.isEmpty():
        
        #taking the frames out to display them (cant display because error in library)
        frame = grayScaleQueue.deque()
        print(f'Displaying frame {count}')

        # cv2.imshow('Video', frame)   #Problem here with library using threads and displaying the frames
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print('Finished displaying all frames')
    cv2.destroyAllWindows()


def main():
    #initializing threads and queues of frames
    filename = 'clip.mp4'
    framesQueue = Queue()
    grayScaleQueue = Queue()
    extraction_t = threading.Thread(target=extract_frames, args=(filename, framesQueue, 72,))
    extraction_t.start()
    conversion_t = threading.Thread(target=convert_to_grayscale, args=(framesQueue, grayScaleQueue,))
    conversion_t.start()
    display = threading.Thread(target=display_frames, args=(grayScaleQueue,))
    display.start()
    display.join()


if __name__ == "__main__":
    main()
