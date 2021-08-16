# Readme Vernissage Pipeline

## GPU

Terminal -> nvtop

 * GPU1 sollte angezeigt werden

    * sonst richtig einstecken, einschalten, neustarten

      

## PIPELINE

* run: python3 vernissage_pipeline.py

* drop dir is where the images go

* pipeline.run(): run the pipeline once

* yet to come: pipeline.handle(): run the pipeline at specific condition eg. N images, Time, key input 

  ### Ordnerstruktur

  --

  ### Material
  
* **Noch Kaufen**

    * schwarzes Ducktape

* Photostation

   * MFK
      * Tisch
      * Licht
      * Stuhl
   * MRT
      * ~~Photobox mit Raspberry Pi netzstecker~~
      * ~~TV gross~~
      * ~~HDMI Kabel kurz~~
      * ~~Buzzer~~
      * ~~Steckleiste mind. 4 Stecker~~
      * ~~Molton~~

 * Büro

     * MFK
         * Tisch
         * zwei Stühle
     * MRT
        * Lenovo Laptop und Netzstecker, Ethernet Adapter?
        * ext. GPU inkl alle Kabel
        * Router inkl Netzstecker
        * ~~Bürolampe schwarze Klemmlampe~~
        * ~~Sticker~~
        * ~~Visitenkarte~~

* Fotodisplay

    * MFK
        * grosser TV	
    * MRT
        * ~~HDMI-Kabel lang sehr lang~~

* Diverses

  * ~~Ethernerkabel 1x lang 1x kurz~~
  * ~~Farbiges Klebeband für Markierungen Wand und Boden~~
   * ~~Verlängerungskabel~~
   * ~~Zweifachstecker~~
   * **Ducktape**
   * ~~Kabelbinder~~
   * ~~Klebeband~~

# Todos

- Photobox bauen (Flügu) Ende März
	- erledigt
- Backup auf HD (Flügu) sofort
- Zeugs auf Dropbox oder GIT ohne 50GB (Flügu) sofort
	- github erldigt
- Preview beim Buzzer mit overlay (Flügu) Ende März
	- erledigt
- Ni an Diashow erinnern (Flügu) Mitte April
- Buzzer antirutsch (Flügu)  -> Teppich klepebeand
- Diashow (Ni) Mitte April 
  - Skalierung möglich vergössern max. oder in prozent einstellen
  - bsp wenn X min nichts passiert random aus allen fotos sonst die neusten Y oder so
- Pipeline handler (Ni) 
	- erledigt

# 

* Color Historram Transfert zwischen Background und Foreground
  * Haben wir jetzt mit Colorgrading manuel gelöst
* Error: Gibt kein Errorchecking 
  * Ist implementiert, noch testen
* Dims: Falls die Fotos andere Dimensionen haben braucht es diesen Schritt noch. Pipeline akzeptier 1920x1280 
* Readme
* Gif wäre schon noch Cool

# Notizen

## 26.02.21

habe pipeline gestartet. dann kam das

```
---- tensorman run --gpu -- python evaluate.py     --checkpoint ./checkpoints/useForEvaluation/LargerTrainingDataSet_Train2014_and_WIDER_train_and_OI_Challenge_neonMask_epoches_8/     --in-path ./input-image/     --out-path ./pipelineOutput/     --allow-different-dimensions
"docker" "run" "-u" "1000:1000" "--gpus=all" "-e" "HOME=/project" "-it" "--rm" "-v" "/home/simonflueckiger/Documents/01_MRT/MfK_Vernissage-Super/PIPELINE/fast-style-transfer:/project" "-w" "/project" "tensorflow/tensorflow:latest-gpu" "python" "evaluate.py" "--checkpoint" "./checkpoints/useForEvaluation/LargerTrainingDataSet_Train2014_and_WIDER_train_and_OI_Challenge_neonMask_epoches_8/" "--in-path" "./input-image/" "--out-path" "./pipelineOutput/" "--allow-different-dimensions"
Unable to find image 'tensorflow/tensorflow:latest-gpu' locally
latest-gpu: Pulling from tensorflow/tensorflow
```

hat dann gaaaanz viel abengeladen

-> sollte man eine bestimte tensorflow version benutzen und nicht `tensorflow:latest-gpu`?