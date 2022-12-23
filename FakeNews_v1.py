#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 06:46:35 2022

@author: leo
"""

import os, sys
try : 
    sys.path.insert(1, os.path.dirname(__file__)+'/images_QCM')
except:
    pass

import random as rd 

import tkinter as tk


# -------------------------------------- 

indice_confiance_minimal_forcage = 30 # %  

try :
    doss_init = os.path.dirname(__file__)
except : 
    doss_init = './'
# -------------------------------------- 

nombre_images_a_proposer = 30


class Annexes() : 
    
    global nombre_images_a_proposer
    
    def __init__(self):
        self.creation_dossier('./__tmp__')
        pass
    
    def stop(self, text = ''):        
        print('\n\n___________________________________________________')
        raise ValueError("stop _ "+text)

    def existence_entite(self, entite):  
        if os.path.exists(entite):
            return entite, True
        return None, False
    
    def creation_dossier(self, dossier):        
        if not os.path.exists(dossier):
            try:
                os.makedirs(dossier)
            except:
                print(f"Erreur ! Impossible de creer {dossier} ")          
        return None
    
    
    def listing_(self, dossier):        
        f = []
        for (dirpath, dirnames, filenames) in os.walk(dossier):
            f.extend(filenames)
            break                
        rd.shuffle(f)
        return f[:nombre_images_a_proposer]


    def verif_integrity(self,s) :     
        try: 
            int(s)
            return True
        except ValueError:
            return False
        
    def sauvegarde(self,x, y, liste = None):
        if liste != [] and liste is not None:              
            
            liste[0] = liste[0] + ' ' + str(x)+'/'+str(y)
            
            Alphab = '0123456789abcdefghijklm_nopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            len_ = len(Alphab)-1            
            from datetime import datetime            
            file_ = '!'+str(int(datetime.timestamp(datetime.now())))+'.zet'
            for i in range(9):            
                file_ = Alphab[rd.randint(0,len_)] + file_                     
            print("\n------------------------\n-- Ecriture de : ")
            with open('./__tmp__/'+file_, 'w', encoding="UTF-8") as writer:
                for ligne in liste : 
                    print(ligne)
                    writer.write(ligne)     
                    writer.write("\n")
                    
# -------------------------------------- 

class Bayesian_Core(Annexes):
    
    def __init__(self):
        
        Annexes.__init__(self)
        self.score = 0
        self.reponses = {'id' : {'nom' : None, 'prenom' : None, 'classe' : None, 'statut' : None, 'idx' : 0}, 'correspondances' : {'statut': None} }        
        self.liste_images = self.listing_(doss_init+'/images_QCM') 
                   
        self.pictures_scoring_init()
        
        self.nombre_reponses = 0
        
        self.numero_image_actuel = 0
        
        self.sauvegarde_non_effectuee = False

        
                
    def reinitialisation_des_images(self):        
        self.reponses['id']['idx'] = 0        
        self.nombre_reponses = 0
        for image in self.liste_images:
            if self.reponses[image]['statut'] is not None :                    
                self.reponses[image]['sens'] = None
                self.reponses[image]['value'] = None 
        
        
    def remelange_images(self):
        liste_temp = self.liste_images.copy()
        rd.shuffle(liste_temp)
        self.liste_images = liste_temp
    
    def analyscoring(self):
        if self.nombre_reponses > 0 : 
            #print("\n ----------SCORING------------- ")        
            nb_question = 0        
            for cle in self.reponses.keys():
                _base_sample = self.reponses[cle]
                
                if _base_sample['statut'] is not None : 
                    
                    if _base_sample['sens'] is not None :     
                        #print(cle.split('description_')[1], end = ' : ')
                        nb_question += 1
                        if _base_sample['value']<indice_confiance_minimal_forcage:
                            _base_sample['value']= indice_confiance_minimal_forcage
                        score_temp = round(0.5*(1+_base_sample['sens']*_base_sample['integrite']*_base_sample['value']*0.01),4)             
                                                
                        #print(_base_sample['integrite'], _base_sample['sens'], _base_sample['value'], score_temp)                                            
                    
                        self.reponses['id']['idx'] += score_temp
                    
            if nb_question >0:
                self.reponses['id']['idx'] = round(100*self.reponses['id']['idx']/nb_question, 1)
    def get_score(self):
        return self.reponses['id']['idx']
               
    def pictures_scoring_init(self):                 
        
        numero_image_viable = 0
        for image in self.liste_images:                
            self.reponses[image] = {'integrite' : -1, 'sens' : None, 'value' : None, 'position_x' : None,  'statut' : None, 'modifiee' : None }             
            _base_score = image.split('e')[1][0]                 
            if self.verif_integrity(_base_score):          
                self.reponses[image]['statut'] = 0
                tmp_cal = int(0.1*(int(_base_score)+5))
                if tmp_cal == 1 :
                    self.reponses[image]['integrite'] = 1   
                self.reponses['correspondances'][numero_image_viable] = image
                numero_image_viable += 1 

                     
            else:
                print(f"non conformite de {image}")
        self.nombre_images_viables = numero_image_viable 
        
    def get_nombre_images_viables(self):
        return self.nombre_images_viables
    
    def sauvegarde_reponses(self):        
        
        if not self.sauvegarde_non_effectuee : 

            lignes_a_ecrire = [str(self.reponses['id']['nom'])+' '+str(self.reponses['id']['prenom'])+' '+str(self.reponses['id']['classe'])]
            x, y = 0, 0
            if self.nombre_reponses > 0 :             
                for cle in self.reponses.keys():
                    _base_rep = self.reponses[cle]
        
                    if _base_rep['statut'] is not None : 
                        y += 1
                        if _base_rep['sens'] is not None and  _base_rep['value'] is not None : 
                            x += 1                    
                            ligne_tmp = ' Pour "'                    
                            temp_ = cle.split('_description_')[1].split('.jpg')[0].split('_')
                            alpha = ''
                            for val in temp_:
                                alpha += val+' '
                            ligne_tmp = ligne_tmp + alpha[:-1] + '" vous avez repondu '
                            
                            if _base_rep['sens'] == 1 :
                                beta = '"probablement vrai"'
                            elif _base_rep['sens'] == -1 :                    
                                beta = '"probablement faux"'
                            else:
                                beta = 'None'                    
                            ligne_tmp = ligne_tmp + beta + ' avec un indice de confiance de ' + str(_base_rep['value']) + ' %'                    
                            lignes_a_ecrire.append(ligne_tmp)     
                        
            lignes_a_ecrire.append(f"Votre score final est de {self.reponses['id']['idx']}/100")                
            self.sauvegarde(x,y,lignes_a_ecrire)
            self.sauvegarde_non_effectuee = True
                    
        
    def enregistrement_reponse(self, image_numero, sens, indice_de_confiance, position_x):
        
    
        self.nombre_reponses += 1 
        self.reponses[self.reponses['correspondances'][image_numero]]['sens'] = sens
        self.reponses[self.reponses['correspondances'][image_numero]]['value'] =  indice_de_confiance        
        self.reponses[self.reponses['correspondances'][image_numero]]['position_x'] = position_x
        
        
    def redonne_reponse(self, image_numero):
        
        reponses = None
        
        if self.reponses[self.reponses['correspondances'][image_numero]]['sens'] is not None : 
           reponses = self.reponses[self.reponses['correspondances'][image_numero]]['sens'], self.reponses[self.reponses['correspondances'][image_numero]]['value'], self.reponses[self.reponses['correspondances'][image_numero]]['position_x'] 
        
        #print("on renvoie ", reponses)
        return reponses
        
    def enregistrement_id(self,type_, valeur):   
        if type_ in ['nom', 'prenom', 'classe']:
            self.reponses['id'][type_] = valeur
        else:
            self.stop()
            
    def get_image(self, image_numero):        
        #print(image_numero, self.reponses['correspondances'].keys())
        if image_numero in self.reponses['correspondances'].keys()  :            
            #print(self.reponses['correspondances'][image_numero])
            self.numero_image_actuel = image_numero
            return doss_init+'/images_QCM/'+self.reponses['correspondances'][image_numero]
        else:
            return None
            
        
    def montre_dico(self):
        
        for image_num in self.reponses['correspondances'].keys():
            if image_num != 'statut':
                image = self.reponses['correspondances'][image_num]
                print(image_num, self.reponses[image]['sens'],self.reponses[image]['value'])
 
        


                
            
            
        


# x = Core()

# print(" ---- ")

# for item in x.reponses.keys():
#     #print("  ")
#     x.reponses[item]['sens'] = [-1,1][rd.randint(0,1)]
#     x.reponses[item]['value'] = rd.randint(0,100)
#     #print(item)
#     #print(x.reponses[item])
    
# x.analyscoring()
# x.sauvegarde_reponses()

        
        
                    
# -------------------------------------- 

import pygame as pg


white,black,grey, red = (255,255,255),(0,0,0),(120,120,120),(204,0,34)            
mediumseagreen, seagreen = (60,179,113), (46,139,87)
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_FONTAL = 'map'+'oule'
COLOR_ACTIVE = pg.Color('dodgerblue2')
#FONT = pg.font.SysFont("Arial",30)


class InputBox:

    
    def __init__(self, x, y, w, h, type_,  text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pg.font.SysFont("Arial",30).render(text, True, self.color)
        self.active = False
        self.type_ = type_


    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
 
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
  
            
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.color = seagreen
                    
   
                    
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pg.font.SysFont("Arial",30).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
        
        
    def enregistrement(self,base):
        if self.text !='':
            base.enregistrement_id(self.type_, self.text)
            return True
        else:
            pass
            return True
            # print("mettre les identifiants")
            # return False

        




class Button:
    #https://pythonprogramming.altervista.org/buttons-in-pygame/
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text,  pos, font, taille, text_color=(0,0,0), bg=(255,255,255), feedback=""):
        
        self.x, self.y = pos
        self.font = pg.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
            self.change_text(text, text_color,bg)
            
    def set_position(self,pos):
        self.x, self.y = pos
        
 
    def change_text(self, text, text_color=(0,0,0), bg=(255,255,255)):
        """Change the text whe you click"""
        self.enonce = text
        self.color_text = text_color
        self.bg = bg
        self.text = self.font.render(text, 1, pg.Color(text_color[0],text_color[1],text_color[2]))
        self.size =  self.text.get_size()
        self.surface = pg.Surface(self.size)
        self.surface.fill(pg.Color(bg[0],bg[1],bg[2]))
        self.surface.blit(self.text, (0, 0))
        self.rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))
        
    def set_enonce(self,joueur_en_cours):
        text_bis = f"it's the turn of the {joueur_en_cours} king to play ! "
        self.change_text( text_bis,self.color_text, self.bg)
            
    def click(self, event):
        x, y = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:         
                if self.rect.collidepoint(x, y):
                    
                    if self.enonce == 'Quitter':
                        print(" ************** \n *   Bye Bye  *\n ************** \n")
                        #pg.quit()
                        return True                    
                    elif self.enonce == 'Recommencer (1 fois)':
                        print(" ********************* \n *   Restarting ...  *\n ********************* \n\n")
                        return True
                    # elif self.enonce in ['rook', 'queen', 'bishop', 'knight']:
                    #     return True
                    
                    elif self.enonce == 'Question suivante':
                        #print("image suivante")
                        return True
                    
                    elif self.enonce == 'Question precedente':
                        #print("image suivante")
                        return True
                    
                    elif self.enonce == 'Erreurs':
                        return True
                    
                    elif self.enonce == 'Terminer le test':
                        return True
                   
                return False




class Curseur : 
    
    def __init__(self, position_x, position_y, largeur):
        self.largeur_initiale = largeur
        self.rect = pg.Rect((position_x-largeur/2, position_y-largeur/2, largeur, largeur ))
        self.position_y = position_y
        self.position_x = position_x
        self.position_x_init = position_x
        self.click = False
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill(seagreen)

        
        
        
    def set_limites_en_x(self,xmin,xmax):
        
        self.xmin = xmin
        self.xmax = xmax
        
    def update(self):
        if self.click:
            x = pg.mouse.get_pos()[0]
            if self.xmin<=x<=self.xmax:          
                
                self.rect.center = (x,self.position_y)
                self.position_x = x
                
                return True
        
    def changement_curseur(self,gameDisplay, pourcentage = None, x = None, y = None, largeur_ = None):       
        
        if pourcentage is not None : 
            largeur = self.largeur_initiale *(1+pourcentage/100)          
        elif largeur_ is not None : 
            largeur = largeur_
        
        if x is None : 
            x = self.rect.x
        else:
            self.position_x = int(x+largeur/2)
            
        if y is None : 
            y = self.rect.y
            
            


        self.rect = pg.Rect((x, y, largeur, largeur))
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill(seagreen)
        
        gameDisplay.blit(self.image,self.rect)
        
    def draw_curseur(self, gameDisplay):                
        gameDisplay.blit(self.image,self.rect)
        
    def reinit_curseur(self, gameDisplay, dico_positions = None):    
        
        if dico_positions is None : 
           
            self.changement_curseur(gameDisplay, 0,self.position_x_init-self.largeur_initiale/2, self.position_y-self.largeur_initiale/2, None)
            
        else:           
            
            self.changement_curseur(gameDisplay, None ,dico_positions['x'] , dico_positions['y'], dico_positions['largeur'])
            
            
    def get_data_curseur(self):
        return {'x' : self.rect.x, 'y' : self.rect.y, 'largeur' : self.rect.width}
        
        
        
        




class Echelle:
    
    def __init__(self):
        self.centre_x, self.centre_y = 0, 0

        self.epaisseur = 2
        
        self.position_x = 0
        
        self.curseur = None
        
        self.verit_, self.indice_de_confiance = None, None
        
        self.action_  = False
        
        
    def set_centre(self, width_screen, height_screen):
        self.largeur = 0.6*width_screen
        self.centre_x = 0.35*width_screen
        self.centre_y = 0.85*height_screen      
        self.epaisseur = 20
        
        self.largeur_du_curseur = 40
        
        self.curseur = Curseur(self.centre_x, self.centre_y, self.largeur_du_curseur)
        
        self.curseur.set_limites_en_x(self.centre_x-self.largeur/2-self.largeur_du_curseur, self.centre_x+self.largeur/2+self.largeur_du_curseur)

        
        
    
        
    def indication(self,gameDisplay, text, position_x, position_y, taille = 20):
        
        indic = pg.font.SysFont("Arial",taille).render(text, True, black)
        textRect_indic = indic.get_rect()
        textRect_indic.center = (position_x, position_y)  
        gameDisplay.blit(indic, textRect_indic)
        
        
    def draw(self, gameDisplay):
        
        changement = self.curseur.update()

        
        verite = None
        
        
        
        if self.curseur.position_x <self.centre_x : 
            verite = 'Fausse'
            self.verit_ = -1
            
        else:
            verite = 'Vraie'
            self.verit_ = 1
            
        self.indice_de_confiance = round(100*self.verit_*(self.curseur.position_x-self.centre_x)/(self.largeur*0.5),0)
        
        if self.indice_de_confiance>100:
            self.indice_de_confiance = 100

        if changement is not None : 
            self.curseur.changement_curseur(gameDisplay, self.indice_de_confiance)
            self.action_ = True
        

        deplacement = 70
        self.indication(gameDisplay, "Vous pensez que l'information est ",self.centre_x-0.3*self.largeur,self.centre_y+ deplacement )
        self.indication(gameDisplay, verite, self.centre_x-0.07*self.largeur,self.centre_y+deplacement, taille = 40)
        self.indication(gameDisplay, ", vous en êtes sûr.e à ", self.centre_x+0.1*self.largeur, self.centre_y+deplacement)
        self.indication(gameDisplay, f"{self.indice_de_confiance} % ",self.centre_x+0.28*self.largeur ,self.centre_y+deplacement, taille = 40)           
            
        self.curseur.draw_curseur( gameDisplay )        
        
        pg.draw.rect(gameDisplay,black,[self.centre_x-self.largeur/2,self.centre_y,self.largeur,2],1)
        
        for i in [1,-1]:
            pg.draw.polygon(gameDisplay, black, ((self.centre_x+i*self.largeur/2,self.centre_y),(self.centre_x+i*self.largeur/2,self.centre_y+10),(self.centre_x+i*self.largeur/2+i*10,self.centre_y),(self.centre_x+i*self.largeur/2,self.centre_y-10),(self.centre_x+i*self.largeur/2,self.centre_y)), 3)
            
            for j in range(0,10):
   
                pg.draw.rect(gameDisplay,black,[self.centre_x+i*j*self.largeur/20-2,self.centre_y-10,self.epaisseur//5,self.epaisseur], width = 0)
                                            
                self.indication(gameDisplay, str(10*abs(i*j)),self.centre_x+i*j*self.largeur/20, self.centre_y+30) 

        
        
                
        self.indication(gameDisplay, "votre confiance dans votre jugement sur la véracité / fausseté de cette information est de ", self.centre_x, self.centre_y-60)
                
        self.indication(gameDisplay, "F ",self.centre_x-0.53*self.largeur,self.centre_y, taille = 40)        
        self.indication(gameDisplay, "V ",self.centre_x+0.54*self.largeur,self.centre_y, taille = 40)
        
                
    
    def positions_curseur(self):        
        return self.curseur.get_data_curseur()
        
        
    
    def get_sens(self):
        return self.verit_
    def get_indice_de_confiance(self):
        return self.indice_de_confiance
    
    
    def reinitialisation(self, gameDisplay, anciennes_reponses):
        
        if anciennes_reponses is None : 
            
    
            self.curseur = Curseur(self.centre_x, self.centre_y, self.largeur_du_curseur)
            
            
            self.indice_de_confiance = 0
            self.verit_ = 1

            
        else:
            self.verit_ = anciennes_reponses[0]
            self.indice_de_confiance = anciennes_reponses[1]
            
            dico_positions = anciennes_reponses[2]           
            
            self.curseur.reinit_curseur(gameDisplay, dico_positions)
            
            
        self.curseur.set_limites_en_x(self.centre_x-self.largeur/2-self.largeur_du_curseur, self.centre_x+self.largeur/2+self.largeur_du_curseur)
            
            
            
            



def transformScaleKeepRatio(image, size):
    iwidth, iheight = image.get_size()
    scale = min(0.70*size[0] / iwidth, 0.70*size[1] / iheight)
    #scale = max(size[0] / iwidth, size[1] / iheight)
    new_size = (round(iwidth * scale), round(iheight * scale))
    scaled_image = pg.transform.smoothscale(image, new_size) 
    #image_rect = scaled_image.get_rect(center = (size[0] // 2, size[1] // 2))
    
    x = 0.01*size[0]
    if new_size[0]<0.70*size[0]:
        x  = (0.7*size[0]-new_size[0])//2
    
    
    image_rect = (x, 0.01*size[1])

    
    return scaled_image, image_rect


    

        
def show(pstrd,app): 
    
    if pstrd.get() == COLOR_FONTAL :

        app.destroy()
        main()
        
def main():         
    
    
    base = Bayesian_Core()              
    width_, height_ = 1600, 900
    
    nombre_images = base.get_nombre_images_viables()
    
    
    pg.init()                 
    #set display
    gameDisplay = pg.display.set_mode((width_, height_),pg.RESIZABLE)

    pg.display.set_caption("Fausses informations, vraies questions")  
    
    
    clock = pg.time.Clock()
    
    input_boxes = [ ]
    
    # ---- pour le nom : 
    nom = pg.font.SysFont("Arial",25).render("Nom : ", True, black)
    textRect_nom = nom.get_rect()
    textRect_nom.center = (0.86*width_, height_*0.4)  
    input_box1 = InputBox(0.85*width_, height_*0.43, 150, 40, 'nom')
    input_boxes.append(input_box1)
    
    # ---- pour le prenom : 
    prenom = pg.font.SysFont("Arial",25).render("Prenom : ", True, black)
    textRect_prenom = prenom.get_rect()
    textRect_prenom.center = (0.86*width_, height_*0.50)  
    input_box2 = InputBox(0.85*width_, height_*0.53, 150, 40, 'prenom')
    input_boxes.append(input_box2)
    
    # ---- pour la classe : 
    classe = pg.font.SysFont("Arial",25).render("Classe : 2nd", True, black)
    textRect_classe = classe.get_rect()
    textRect_classe.center = (0.86*width_, height_*0.6)  
    input_box3 = InputBox(0.85*width_, height_*0.63, 150, 40, 'classe')
    input_boxes.append(input_box3)
    
    indication = pg.font.SysFont("Arial",15).render(f"L'indice de confiance sera toujours considéré comme étant supérieur ou égal à {indice_confiance_minimal_forcage}% par défaut dans le calcul du score ", True, black)
    textRect_indication = indication.get_rect()
    textRect_indication.center = (width_//4, 0.97*height_) 
    
    # ---- quelques boutons : 
    restart_button = Button("Recommencer (1 fois)",(0.83*width_, height_*0.10),font=25,taille = 0, text_color=(0,0,0), bg=(255,255,255),feedback="You clicked me")    
    quit_button = Button("Quitter",(0.85*width_, height_*0.2),font=25, taille =50, text_color=(0,0,0), bg=(255,255,255),feedback="You clicked me")
    
    suivant_button = Button("Question suivante",(width_*0.8, height_*0.95),font=25, taille =50, text_color=(0,0,0), bg=(255,255,255),feedback="You clicked me")
    precedent_button = Button("Question precedente",(width_*0.8, height_*0.9),font=25, taille =50, text_color=(0,0,0), bg=(255,255,255),feedback="You clicked me")
    
    #fin_button = Button("Terminer le test",(width_*0.8, height_*0.85),font=25, taille =10, text_color=(0,0,0), bg=(255,255,255),feedback="You clicked me")
    
    
    display_erreur_button = Button("Erreurs",(width_*0.8, height_*0.05),font=25, taille =50, text_color=(0,0,0), bg=(255,255,255),feedback="You clicked me")
    
    
    
    echelle = Echelle()
    echelle.set_centre(width_, height_)
    
    
    
    
    gameExit = False   
    affichage_score = False
    recommencement = 1
    
    
    
    image_numero = 0

    image_path = base.get_image(image_numero)
    if image_path is not None : 
        current_image = pg.image.load(image_path).convert() 
        current_image, bg_rect = transformScaleKeepRatio(current_image, gameDisplay.get_size())
        
    else:
        print("Aucune image de viable, on quitte")
        gameExit = True
    
    while not gameExit :              
        

        gameDisplay.fill((255, 255, 255))
        
        if not affichage_score:
        
            nombre_images_text = pg.font.SysFont("Arial",20).render(f"image {image_numero+1} / {nombre_images}", True, black)
            gameDisplay.blit(nombre_images_text,(width_*0.85, height_*0.8))
            

            gameDisplay.blit(indication, textRect_indication)
            
            gameDisplay.blit(current_image, bg_rect)
    
            echelle.draw(gameDisplay)
            
        gameDisplay.blit(nom, textRect_nom)
        gameDisplay.blit(prenom, textRect_prenom)
        gameDisplay.blit(classe, textRect_classe)
        


        for event in pg.event.get():              
     
            ## ---- si on doit quitter le jeu
            if event.type == pg.QUIT or quit_button.click(event)  : 
                #pg.quit()
 
                ok_ = False
                for box in input_boxes:
                    if not ok_:
                        ok_ = box.enregistrement(base)
                        
                        
                if ok_:
                    gameExit = True   
                    if echelle.action_ :
                        base.enregistrement_reponse(image_numero, echelle.get_sens(), echelle.get_indice_de_confiance(), echelle.positions_curseur())
                        echelle.action_  = False                       
                    base.analyscoring()
                    base.sauvegarde_reponses()
                    
                
            
            elif restart_button.click(event) and recommencement == 1 :
                for box in input_boxes:
                    box.enregistrement(base)
                recommencement = 0
                image_numero = 0
                base.analyscoring()
                base.sauvegarde_reponses()                
                base.remelange_images()
                base.reinitialisation_des_images()
                gameExit = True
                
            elif event.type == pg.VIDEORESIZE:
                gameDisplay = pg.display.set_mode(event.size, pg.RESIZABLE)
                current_image, bg_rect = transformScaleKeepRatio(current_image, gameDisplay.get_size())
                gameDisplay.fill((255, 255, 255))
                
            elif display_erreur_button.click(event):
                
                base.montre_dico()
                
            elif suivant_button.click(event) :
                image_path = base.get_image(image_numero+1)
                if image_path is not None : 
                    
                    if echelle.action_ :
                        base.enregistrement_reponse(image_numero, echelle.get_sens(), echelle.get_indice_de_confiance(), echelle.positions_curseur())
                        echelle.action_  = False
                        
                    image_numero += 1
                    current_image = pg.image.load(image_path).convert() 
                    current_image, bg_rect = transformScaleKeepRatio(current_image, gameDisplay.get_size())
                    
                    echelle.reinitialisation(gameDisplay, base.redonne_reponse(image_numero))
                    
                    
                elif image_numero+1 == nombre_images : 
                    ok_ = False
                    for box in input_boxes:
                        if not ok_ : 
                            ok_ = box.enregistrement(base)
                    if ok_ :
                        affichage_score = True
                        if echelle.action_ :
                            base.enregistrement_reponse(image_numero, echelle.get_sens(), echelle.get_indice_de_confiance(), echelle.positions_curseur())
                            echelle.action_  = False

                        base.analyscoring()
                        base.sauvegarde_reponses()
                        image_numero += 1
                
            elif precedent_button.click(event) :          
                image_path = base.get_image(image_numero-1)
                if image_path is not None : 
                    if echelle.action_ :
                        base.enregistrement_reponse(image_numero, echelle.get_sens(), echelle.get_indice_de_confiance(), echelle.positions_curseur())
                        echelle.action_  = False
                    image_numero -= 1           
                    current_image = pg.image.load(image_path).convert() 
                    current_image, bg_rect = transformScaleKeepRatio(current_image, gameDisplay.get_size())                   
                    
                    echelle.reinitialisation(gameDisplay, base.redonne_reponse(image_numero))
                    
            elif event.type == pg.MOUSEBUTTONDOWN:
   
                if echelle.curseur.rect.collidepoint(event.pos):
 
                    echelle.curseur.click = True
            elif event.type == pg.MOUSEBUTTONUP:
                echelle.curseur.click = False

            for box in input_boxes:
                box.handle_event(event)
                
        if not gameExit:
            
            for box in input_boxes:
                box.update()
                
            for box in input_boxes:
                box.draw(gameDisplay)
    
            #pg.display.flip()
            quit_button.show(gameDisplay)
            restart_button.show(gameDisplay)
            
            if affichage_score:                
                score_final = base.get_score()
                echelle.indication(gameDisplay, "Votre score final est de  ",width_//2,height_//3, taille = 40) 
                echelle.indication(gameDisplay, f"{score_final} % ",width_//2, 1.5*height_//3, taille = 80) 
                
                humour_fin = ''
                if 0 == score_final : 
                    humour_fin = 'La boulette ! Le prof va vous mettre 0 ! '
                    
                elif 0<score_final<=20: 
                    humour_fin = 'DANGER ZONE !! Soyez Critique dans vos réflexions ! Comme votre mirroir, réfléchissez ! '
                    
                elif 20<score_final<=40:
                    humour_fin = 'Vous êtes le planplan de rantanplan niveau réflexion, soyez plus fin limier !'
                    
                elif 40<score_final<=60:
                    humour_fin = "Un peu frileux du cerveau, mais l'incertitude est préférable. Faîtes gaffe quand même ! Un accident est si vite arrivé"
                    
                elif 60<score_final<=80:
                    humour_fin = "Vous êtes plus Watson que Sherlock ! Bravo, essayez de faire mieux quand même ! "
                    
                elif 80<score_final<=90:
                    humour_fin = "Ah pas mal !! Vous ne tombez pas dans le panneau facilement ! Félicitations ! "
                    
                else:
                    humour_fin = "What the Flute of the coconut ??? Excellent mon Eminence ! Congrats !! "
                    
                echelle.indication(gameDisplay, f"{humour_fin} ",width_//2, 2*height_//3, taille = 20) 
                
        
            else:

                if image_numero != nombre_images : 
                    suivant_button.show(gameDisplay)
                    
                precedent_button.show(gameDisplay)
            #display_erreur_button.show(gameDisplay)
            

            
            
            width_, height_ = gameDisplay.get_size()
            
            # suivant_button.set_position((width_*0.85, height_*0.95))
            # precedent_button.set_position((width_*0.85, height_*0.9))

                        
            
            textRect_indication.center = (width_//2, height_-20) 
            
            
            clock.tick(30) #fps rafraichissement
            pg.display.update()    
        
                         
        
                    
    pg.quit()
    sys.exit()
    
def lancement():
    
    app = tk.Tk()   
    pstrd = tk.StringVar() #Password variable
    passEntry = tk.Entry(app, textvariable=pstrd, show='*')
    submit = tk.Button(app, text='Show Console',command=show(pstrd,app))
    
    
    passEntry.pack() 
    submit.pack()      
    
    app.mainloop() 
    
    
    
if __name__ == "__main__":     
    if False:
        lancement()                 
    
    else:
        main()