import cv2
import numpy as np

lo=np.array([95, 100, 50])
hi=np.array([105, 255, 255])
cap=cv2.VideoCapture(0) #recuperation du flux video de la webcam(camera)
while (True):
    #recuperation de deux valeur un retour et la frame 
    #qui est l image elle meme et la 1ere chose à faire c est de passer l image 
    #recuperé de la webcam,
    ret, frame=cap.read() 

    #nous allons faire un changement 
    #d espace colorimetrique de BGR à HSV.
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #fonction couleur inRange avec qui on a donné
    # une couleur minimum et maximum ainsi qu une image et qui va nous renvoyer 
    #un masque n extrayant la couleur demandée
    #bleu ==  100
    mask=cv2.inRange(image, lo, hi)

    ###Ajout d un peu de flou à l image pour ameliorer eton lui donne une taille
    ##du Kernel plus on met un kernel gros plus le flou sera fort
    image=cv2.blur(image, (7, 7))

    ##Application d erode
    mask=cv2.erode(mask, None, iterations=4)

    ##Application de dilate
    mask=cv2.dilate(mask, None, iterations=4)

    # verification de ce que 
    #donne l image auquelle on applique le mask:creation d image qui va afficher
    #le resultat d un et logique (bitwise_and) on lui donne limage de la camera
    #2 fois le et va se faire entre l image et l image elle meme seulement 
    #lorsque le masque serait egual à 255
    image2=cv2.bitwise_and(frame, frame, mask=mask) 

    #### Utlilisation de la fonction findContour pour demander des formes
    ####qu'elle detecte dans l'image sans lui demander des sous formes qui
    ####pourrait etre dans les formes detectées
    ####on lui donne le mask et 2 elements et dans l avant derniere element 
    ##du tableau on aura lensemble des formes que cette fonction a trouvée

    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(elements) > 0:#verification si le nombre des formes et au moins egual à 1
        c=max(elements, key=cv2.contourArea)#renvoi de l element le plus grand
        ((x, y), rayon)=cv2.minEnclosingCircle(c)#donne le cercle dans lequel cette forme se trouve
        ##renvoi une coordonnée et un rayon
        if rayon>30:##on prend les objet avec une certaine taille
            ##On dessine le cercle que nous renvoie cette fonction et on le met
            ##Dans l image 2 et le frame
            cv2.circle(image2, (int(x), int(y)), int(rayon), color_infos, 2)
            cv2.circle(frame, (int(x), int(y)), 5, color_infos, 10)
            cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_infos, 2)
            cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_infos, 1, cv2.LINE_AA)
            

    cv2.imshow('Camera', frame)#affichage image brute
    cv2.imshow('image2', image2)#affichage image2
    cv2.imshow('Mask', mask)#affichage du masque

    # sortie du programme lorsque nous appuiyons sur q
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()#liberer toutes les ressourses hardware
cv2.destroyAllWindows()#detruit toute les fenetres  crees dans ce programme

##   problème : il y a plein de petit groupe de pixel bleu
## on doit nettoyer avec erode(on lui donne  le masque et elle va renier 
# les formes autant de fois qu on lui demande d appliquer l algorithme)
## et avec dilate on va rajouter de nouveau des pixels
##

