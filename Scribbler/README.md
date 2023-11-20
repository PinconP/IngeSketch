# IngeSketch 

IngeSketch est assistant de dessin permettant de ganarer une image à partir d'un promprt et d'un dessin peu élaboré réalisé par l'utilisateur. Il est également muni d'un agent conversationnel permettant de guider l'utilisateur dans son utilisation de l'application

Le Scribbler est une composante de l'application IngeSketch qui permet à l'utilisateur de dessiner sur une fenêtre pop-up. Une fois le dessin effectué, l'image générée est renvoyée pour un usage ultérieur.

## Fonctionnalités 

Interface de dessin pop-up : 
Ouvre une fenêtre pop-up où l'utilisateur peut effectuer des dessins.

Capture du dessin : 
Enregistre le dessin effectué par l'utilisateur.

Conversion en image : 
Convertit le dessin en une image au format PIL (Python Imaging Library).

Enregistrement local : 
Sauvegarde l'image générée localement pour permettre à l'utilisateur de l'afficher ultérieurement.

## Prerequis 

Python 3 
Libs : ingescape, opencv-python, numpy, pillow, matplotlib, SpeechRecognition

## Entrées 
Impulsion (IMPULSION_T) : 
L'entrée principale, déclenchant le processus de dessin. Lorsque cette impulsion est reçue, la fenêtre pop-up de dessin s'ouvre.

## Sorties 

Scribble (DATA_T) : 
Les données du dessin de l'utilisateur, converties en format binaire (pickled) pour être renvoyées.

Chemin du dessin (STRING_T) : 
Le chemin local où l'image générée est sauvegardée en format PNG. Ce chemin est fourni pour permettre à l'utilisateur de localiser et afficher l'image ultérieurement.

## Utilisation 
