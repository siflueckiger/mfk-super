import java.*;
import java.io.FilenameFilter;

/*

 ToDo:
 - imagesInit Function 
 - Sampling Function
 - Take N newest images till Change 
 - Grid Mode: Boarder correction 
 
 */

FilenameFilter endsWithPng = new FilenameFilter() {
  public boolean accept(File dir, String name) {
    String lowercaseName = name.toLowerCase();
    //println(name);
    if (lowercaseName.endsWith(".png")) {
      return true;
    } else {
      return false;
    }
  }
};

boolean SIM = false; //true: simulate the big screen on a Window halfe the size of 4K -> see size() in setup
//       images half the original size are in the folder ImagesSmall for simulation
//false: sketch is run on the big screen in real condition, with original size Images and on fullscreen

int MODE = 3; // 1: Single image in the Center of the screen, No Scaling -> consider setting the boardersize to 0.
// 2: Single image in the Center of the screen, with Up-Scaling
// 3: Four images, No Scaling 

float BOARDERSIZE = 0.05; //size of the boarder around the images, a small downscaling factor, relativ to the image- width and -heigth.
float DISPLAYTIME = 3; //Time one image is displayed in seconds

String imagesDirPath;


String[] imagePaths;
IntList imageIndex = new IntList();
File imageDir;

PImage img;

int imgI = 0;
int countSinceInit = 0;

int repetitionsSinceInit = 3;

float boarderSize = 1.-BOARDERSIZE; //  boardersize
int imageWidth = 1920;
int imageHeight = 1280;

void settings() {


  if (SIM) {
    size(1920, 1080);  // my display  2880 x 1800  dest: 3840 x 2160 -> sim at 1920 x 1080 with images 960 x 640
    imagesDirPath = sketchPath() + "/ImagesSmall/";
  } else {
    fullScreen();
    // imagesDirPath = sketchPath() + "/ImagesSmall/";
    imagesDirPath = "/home/simonflueckiger/Documents/01_MRT/02_installationen/mfk-super/PIPELINE/Vernissage_pipeline/output/";
  };
}

void setup() {
  println("datapath: " + dataPath(""));

  imageMode(CENTER);
  background(0);
  imageDir = new File(imagesDirPath);
  initImages();

  takeLastNImages(8);
  //randomImageOrder();
  //imagePaths = sort(imagePaths);
}

void initImages() {
  File[] FileImagePaths = imageDir.listFiles(endsWithPng);
  //println(FileImagePaths.length);

  imagePaths = new String[FileImagePaths.length];
  imageIndex = new IntList();
  for (int i = 0; i < FileImagePaths.length; i++) {
    imagePaths[i] = FileImagePaths[i].toString();
    imageIndex.append(i);
  }
  imagePaths = sort(imagePaths);
  imagePaths = reverse(imagePaths);
}

void takeLastNImages(int N) {
  imageIndex = new IntList();
  for (int i = 0; i < N; i++) {
    imageIndex.append(i);
  }
}

void takeAllImages() {
  imageIndex = new IntList();
  for (int i = 0; i < imagePaths.length; i++) {
    imageIndex.append(i);
  }
}

void randomImageOrder() {
  imageIndex.shuffle();
}

void draw() {

  println(imagePaths[imageIndex.get(imgI)]);
  img = loadImage(imagePaths[imageIndex.get(imgI)]);
  imgI++;

  switch(MODE) {
  case 1:
    singleImageOrigSize(img);
    break;
  case 2:
    singleImageUpScaled(img);
    break;
  case 3:
    show4Images(img, imgI);
    break;
  }


  if (imagePaths.length < imageDir.listFiles(endsWithPng).length) {
    initImages();
    takeLastNImages(8);
    //randomImageOrder();
    countSinceInit = 0;
    background(0);
  }
  println(imageIndex);
  //Image show time
  if (countSinceInit > 4) {
    delay((int)(DISPLAYTIME*1000));// LL
  } else {
    delay(300);
  }
  if (imgI >= imageIndex.size()) {
    imgI=0;
  }
  countSinceInit++;
  if (countSinceInit > imageIndex.size()*repetitionsSinceInit) {
    takeAllImages();
    randomImageOrder();
  }
}

/// MODE 1
void singleImageOrigSize(PImage img) {
  img.resize((int)(imageWidth*boarderSize), (int)(imageHeight*boarderSize));
  image(img, width/2., height/2.);
}

/// MODE 2
void singleImageUpScaled(PImage img) {
  img.resize(0, (int)(height*boarderSize));
  image(img, width/2., height/2.);
}

///MODE 3
void show4Images(PImage img, int I) {
  img.resize((int)(imageWidth*boarderSize*0.4), (int)(imageHeight*boarderSize*0.4));
  float horizontalCorrection = 0.02;
  switch(I%4) {
  case 0:
    println("case 0");
    image(img, width*(1/4.+(1.-boarderSize)*0.5+horizontalCorrection), height/4);
    break;
  case 1:
    println("case 1");
    image(img, width*(3./4.-(1.-boarderSize)*0.5-horizontalCorrection), height/4);
    break;
  case 2:
    println("case 2");
    image(img, width*(1/4.+(1.-boarderSize)*0.5+horizontalCorrection), height*(3./4.));    
    break;
  case 3:
    println("case 3");
    image(img, width*(3./4.-(1.-boarderSize)*0.5-horizontalCorrection), height*(3./4.));
    break;
  }
}
