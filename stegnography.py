from PIL import Image

# ENCODER
def ENCODER():
    img = input("Enter full name of image to be encoded : ")
    image = Image.open(img, 'r')

    data = input("Enter string to be encoded into image : ")
    if (len(data) == 0):
        raise ValueError('Enter valid string')
    new_image = image.copy()
       
    x_size = new_image.size[0]
    x = 0
    y = 0
    for pix in EDIT(new_image.getdata(), data):
        # Edit the pixels to add the string
        new_image.putpixel((x, y), pix)
        # putpixel is used to access any pixel in an image with (x,y)
        if (x == x_size - 1):
            x = 0
            y += 1
        else:
            x += 1


    new_img_name = input("Enter name of output image with extension : ")
    new_image.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    main()

# DECODING
def DECODER():
    img = input("Enter full image name to be decoded : ")
    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pix = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pix[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pix[-1] % 2 != 0):
            return data
    main()
        

def EDIT(pix, data):
    datalist = []
    for i in data:
        datalist.append(format(ord(i), '08b')) 
    print(datalist)

    lendata = len(datalist)
    imdata = iter(pix)      # similar to a for loop
    
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
        # imdata is used to get in groups of 3
        # list comprehension, new modified list from imdata is added to pix, value is variable
        # 3 pixels info is taken to be compared and modify with 8-bin binary
        # 3 pixels in (r,g,b)
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
            # If a bit is 0 in 8-bit binary data and iterating through (r1,g1,b1) (r2,g2,b2) (r3,g3,b3) [3 pixels]  is not even

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                # If a bit is 1 in 8-bit binary and iterating through (r1,g1,b1) (r2,g2,b2) (r3,g3,b3) is even
                else:
                    pix[j] += 1
                

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
        # yield is similar to return for link comprehension

# main Function
def main():
    print("\n******************* STEGEASY ********************\n")
    n = int(input("Press 1 to ENCODE a text into image\nPress 2 to DECODE an image containing hidden text\n"))
    if (n == 1):
        ENCODER()

    elif (n == 2):
        print("The Decoded string in the image is: " + DECODER())
    else:
        raise Exception("Enter valid option")

# Driver Code
if __name__ == '__main__' :

    # Calling main function
    main()
