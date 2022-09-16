import fitz

def get_coords_and_coluors(page):
    # loop till we have highlight annotation in the page
    annot = page.first_annot
    # list to store the co-ordinates and coulors of all highlights
    highlight_coulors = []
    while annot:
        if (annot.type[0] == 8 or annot.type[0] == 15) and annot.vertices[0][0] !=annot.vertices[0][1]:
            #extract the colour of the highlight
            rgb_colours = fix_coulor(annot.colors['stroke'])
    
            coord = export_squre_cowardeanates(annot.vertices)
    
            highlight_coulors.append((rgb_colours,coord))
    
        annot = annot.next
    return highlight_coulors



def get_words(highlight_coulors, page):
    all_words = page.get_text_words()
    # List to store all the highlighted texts
    highlight_text = []

    for colour, h in highlight_coulors:
        for word in all_words:
            word_rect=fitz.Rect(word[0:4])
            if word_rect.x0>=(h.x0-2) and word_rect.x1<=(h.x1+2) and word_rect.y0>=(h.y0-8) and word_rect.y1<=(h.y1+2):
                print(word[4], colour )
                highlight_text.append([word[4], colour])
    return highlight_text




def export_squre_cowardeanates(all_coordinates):
    if len(all_coordinates) == 4:
        return fitz.Quad(all_coordinates).rect
    else:
        #find max and min coards
        maxX=all_coordinates[0][0][0]
        minX=all_coordinates[0][0][0]
        maxY=all_coordinates[0][0][1]
        minY=all_coordinates[0][0][1]
        for array1 in all_coordinates:
            for array2 in array1:
                x=array2[0]
                y=array2[1]
                if x>maxX:
                    maxX=x
                elif x<minX:
                    minX=x
                if y>maxY:
                    maxY=y
                elif y<minY:
                    minY=y
        return fitz.Rect(minX,minY,maxX,maxY)



def fix_coulor(present_colours):
    rgb_colours=[]
    #convert it into rgb values
    for pixel in present_colours:
        rgb_colours.append(round(255*pixel))
    return rgb_colours


def main():
    #set up pdf to be checked
    doc = fitz.open("'Booking_Print_AFYGCQY.pdf")# Total page in the pdf
    testPage = doc[1]

    highlightInformation = get_coords_and_coluors(testPage)
    highlight_text = get_words(highlightInformation, testPage)


if __name__ == "__main__":
    main()