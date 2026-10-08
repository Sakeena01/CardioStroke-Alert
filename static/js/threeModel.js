// ==============================
// THREE.JS 3D HUMAN MODEL
// ==============================

import * as THREE from 'https://unpkg.com/three@0.161.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.161.0/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'https://unpkg.com/three@0.161.0/examples/jsm/loaders/GLTFLoader.js';

const canvas = document.getElementById("humanModel");

const scene = new THREE.Scene();

scene.background = null;

const camera = new THREE.PerspectiveCamera(
45,
canvas.clientWidth / canvas.clientHeight,
0.1,
1000
);

camera.position.set(0,1.5,4);

const renderer = new THREE.WebGLRenderer({
canvas:canvas,
alpha:true,
antialias:true
});

renderer.setPixelRatio(window.devicePixelRatio);

renderer.setSize(
canvas.clientWidth,
canvas.clientHeight
);

renderer.outputColorSpace = THREE.SRGBColorSpace;

// Ambient Light

const ambient = new THREE.AmbientLight(0xffffff,2);

scene.add(ambient);

// Blue Light

const blueLight = new THREE.PointLight(0x00d9ff,8);

blueLight.position.set(3,3,3);

scene.add(blueLight);

// Green Light

const greenLight = new THREE.PointLight(0x00ff99,5);

greenLight.position.set(-3,2,2);

scene.add(greenLight);

// Bottom Light

const bottom = new THREE.PointLight(0x0099ff,4);

bottom.position.set(0,-3,0);

scene.add(bottom);

// Orbit

const controls = new OrbitControls(camera,renderer.domElement);

controls.enablePan=false;

controls.enableZoom=false;

controls.autoRotate=true;

controls.autoRotateSpeed=1.5;

// Loader

const loader=new GLTFLoader();

let human;

loader.load(

"/static/models/human.glb",

function(gltf){

human=gltf.scene;

human.scale.set(2,2,2);

human.position.set(0,-2,0);

scene.add(human);

},

undefined,

function(error){

console.log(error);

}

);

// Animation

function animate(){

requestAnimationFrame(animate);

if(human){

human.rotation.y+=0.002;

human.position.y=Math.sin(Date.now()*0.001)*0.05-2;

}

controls.update();

renderer.render(scene,camera);

}

animate();

// Resize

window.addEventListener("resize",()=>{

camera.aspect=canvas.clientWidth/canvas.clientHeight;

camera.updateProjectionMatrix();

renderer.setSize(

canvas.clientWidth,

canvas.clientHeight

);

});

// Glow Ring

const geometry=new THREE.TorusGeometry(1.3,0.02,16,100);

const material=new THREE.MeshBasicMaterial({

color:0x00d9ff

});

const ring=new THREE.Mesh(geometry,material);

ring.rotation.x=Math.PI/2;

scene.add(ring);

function rotateRing(){

ring.rotation.z+=0.005;

requestAnimationFrame(rotateRing);

}

rotateRing();