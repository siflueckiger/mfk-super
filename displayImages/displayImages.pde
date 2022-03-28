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

int MODE = 5; // 1: Single image in the Center of the screen, No Scaling -> consider setting the boardersize to 0.
// 2: Single image in the Center of the screen, with Up-Scaling
// 3: Four images, No Scaling 
// 4: Collage
// 5: 3x3 images

float BOARDERSIZE = 0.05; //size of the boarder around the images, a small downscaling factor, relativ to the image- width and -heigth.
float DISPLAYTIME = 1.5; //Time one image is displayed in seconds

int NUMBER_OF_IMAGES = 8;

String imagesDirPath;

int case_num = 0;  

// MODE 5
float spacing;
float t_b_margin, l_r_margin;
float img_w, img_h;


String[] imagePaths;
IntList imageIndex = new IntList();
File imageDir;

PImage img;

int imgI = 0;
int countSinceInit = 0;

int repetitionsSinceInit = 3000000;

float boarderSize = 1.-BOARDERSIZE; //  boardersize
int imageWidth = 1920;
int imageHeight = 1280;

void settings() {


  if (SIM) {
    size(1920, 1080);  // my display  2880 x 1800  dest: 3840 x 2160 -> sim at 1920 x 1080 with images 960 x 640
    imagesDirPath = sketchPath() + "/ImagesSmall/";
  } else {
    fullScreen(P2D, 2);
    //size(1920, 1080);
    //imagesDirPath = sketchPath() + "/ImagesSmall/";
    imagesDirPath = "/home/simonflueckiger/Documents/01_MRT/02_installationen/mfk-super/pipelineOutput";
    //imagesDirPath = "../pipelineOutput/";
    //imagesDirPath = "/Users/danielschmocker/Documents/Projekte/Python/mfk-super/pipelineOutput";
  }
}

void setup() {
  println("datapath: " + dataPath(""));

  imageMode(CENTER);
  background(0);
  imageDir = new File(imagesDirPath);
  initImages();
  
  if(MODE == 5){
    t_b_margin = height/17;
    l_r_margin = width / 17;
    spacing = t_b_margin * 0.4;
    float w = (width - (2*spacing) - (2*l_r_margin)) / 3;
    //img_w = (width - (2*spacing) - (2*l_r_margin)) / 3; //imgageWidth * scalefactor = img_w
    float scalefactor =  w / imageWidth*0.85;
    img_w = imageWidth * scalefactor;
    println(img_w);
    //img_h = (height - (2*spacing) - (2*t_b_margin)) / 3;
    img_h = imageHeight * scalefactor;
    println(img_h);
    //exit();

    imageMode(CORNER);
    NUMBER_OF_IMAGES = 12;
  
  }

  takeLastNImages(NUMBER_OF_IMAGES);
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
  case 4:
    showCollage(img, imgI);
    break;
  case 5:
    show9Images(img, imgI);
  }


  if (imagePaths.length < imageDir.listFiles(endsWithPng).length) { // new Images??
    initImages();
    takeLastNImages(NUMBER_OF_IMAGES); //wieviele Bilder
    //randomImageOrder();
    countSinceInit = 0;
    //background(0);
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


//MODE 4
void showCollage(PImage img, int I){
  
  //float horizontalCorrection = 0.02;
  println("case_num: " + case_num + ", img_number: " + I);
  
  
  switch(case_num) {
  case 0:
    //println("case 0");
    img.resize((int)(imageWidth*boarderSize*0.4), (int)(imageHeight*boarderSize*0.4));
    image(img, width/3, height/3);
    case_num++;
    break;
  case 1:
    //println("case 1");
    img.resize((int)(imageWidth*boarderSize*0.35), (int)(imageHeight*boarderSize*0.35));
    image(img, 1.5*width/3, 2.3*height/3);
    case_num++;
    break;
  case 2:
    //println("case 2");
    img.resize((int)(imageWidth*boarderSize*0.25), (int)(imageHeight*boarderSize*0.25));
    image(img, 1.43*width/2, 1.2*height/4);    
    case_num++;
    break;
  case 3:
    //println("case 3");
    img.resize((int)(imageWidth*boarderSize*0.2), (int)(imageHeight*boarderSize*0.2));
    image(img, 1.73*width/2, 2.5*height/4);
    case_num++;
    break;
  case 4:
   //println("case 4");
    img.resize((int)(imageWidth*boarderSize*0.15), (int)(imageHeight*boarderSize*0.15));
    image(img, 0.15*width, 2.7*height/4);
    case_num++;
    break;
  case 5:
    //println("case 5");
    img.resize((int)(imageWidth*boarderSize*0.16), (int)(imageHeight*boarderSize*0.16));
    image(img, 0.2*width, 3.5*height/4);
    case_num = 0;
    break;
  }

}

///MODE 5
void show9Images(PImage img, int I) {
  println("I: " + I + " case_num: " + case_num);
  img.resize(int(img_w), int(img_h));
  float offset = 120.;
  switch(case_num) {
  // row one
  case 0:
    println("case 0");
    image(img, l_r_margin+offset, t_b_margin);
    case_num++;
    break;
  case 1:
    println("case 1");
    image(img, l_r_margin+offset + 1 * (img_w + spacing), t_b_margin);
    case_num++;
    break;
  case 2:
    println("case 2");
    image(img, l_r_margin+offset + 2 * (img_w + spacing), t_b_margin);
    case_num++;
    break;
  
  // row two
  case 3:
    println("case 0");
    image(img, l_r_margin+offset, t_b_margin + 1 * (img_h + spacing));
    case_num++;
    break;
  case 4:
    println("case 1");
    image(img, l_r_margin+offset + 1 * (img_w + spacing), t_b_margin + 1 * (img_h + spacing));
    case_num++;
    break;
  case 5:
    println("case 2");
    image(img, l_r_margin+offset + 2 * (img_w + spacing), t_b_margin + 1 * (img_h + spacing));
    case_num++;
    break;
 
  // row three
  case 6:
    println("case 0");
    image(img, l_r_margin+offset, t_b_margin + 2 * (img_h + spacing));
    case_num++;
    break;
  case 7:
    println("case 1");
    image(img, l_r_margin + offset+ 1 * (img_w + spacing), t_b_margin + 2 * (img_h + spacing));
    case_num++;
    break;
  case 8:
    println("case 2");
    image(img, l_r_margin+offset + 2 * (img_w + spacing), t_b_margin + 2 * (img_h + spacing));
    case_num = 0;
    break;
  }
}
