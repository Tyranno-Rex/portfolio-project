import * as THREE from 'three';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import * as holdEvent from "https://unpkg.com/hold-event@0.2.0/dist/hold-event.module.js";
import CameraControls from './dist/camera-controls.module.js';
CameraControls.install( { THREE: THREE } );

const width = window.innerWidth;
const height = window.innerHeight;
const clock = new THREE.Clock();
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 60, width / height, 0.01, 1000);

camera.position.set(80, 15, 0);
camera.lookAt(new THREE.Vector3(10, 10, 10));

const renderer = new THREE.WebGLRenderer();
renderer.setSize( width, height );
document.body.appendChild( renderer.domElement );

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize( window.innerWidth, window.innerHeight );
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0';
labelRenderer.domElement.style.pointerEvents = 'none'; // 마우스 이벤트를 차단
document.body.appendChild( labelRenderer.domElement );

const cameraControls = new CameraControls( camera, renderer.domElement );
cameraControls.minDistance = cameraControls.maxDistance = 1;
cameraControls.azimuthRotateSpeed = - 0.3; // negative value to invert rotation direction
cameraControls.polarRotateSpeed   = - 0.3; // negative value to invert rotation direction
cameraControls.truckSpeed = 1;
cameraControls.mouseButtons.wheel = CameraControls.ACTION.ZOOM;
cameraControls.mouseButtons.left = CameraControls.ACTION.ROTATE;
cameraControls.mouseButtons.right = CameraControls.ACTION.TRUCK;
cameraControls.touches.two = CameraControls.ACTION.TOUCH_ZOOM_TRUCK;
cameraControls.touches.three = CameraControls.ACTION.TOUCH_PAN;
cameraControls.saveState();

let hoveredLabel = document.createElement('div');
hoveredLabel.className = 'label';
document.body.appendChild(hoveredLabel);

const KEYCODE = {
	W: 87,
	A: 65,
	S: 83,
	D: 68,
	Q: 81,
	E: 69
};

const wKey = new holdEvent.KeyboardKeyHold( KEYCODE.W, 16.666 );
const aKey = new holdEvent.KeyboardKeyHold( KEYCODE.A, 16.666 );
const sKey = new holdEvent.KeyboardKeyHold( KEYCODE.S, 16.666 );
const dKey = new holdEvent.KeyboardKeyHold( KEYCODE.D, 16.666 );
const qKey = new holdEvent.KeyboardKeyHold( KEYCODE.Q, 16.666 );
const eKey = new holdEvent.KeyboardKeyHold( KEYCODE.E, 16.666 );

aKey.addEventListener( 'holding', function( event ) { cameraControls.truck( - 0.05 * event.deltaTime, 0, false ) } );
dKey.addEventListener( 'holding', function( event ) { cameraControls.truck(   0.05 * event.deltaTime, 0, false ) } );
wKey.addEventListener( 'holding', function( event ) { cameraControls.forward(   0.05 * event.deltaTime, false ) } );
sKey.addEventListener( 'holding', function( event ) { cameraControls.forward( - 0.05 * event.deltaTime, false ) } );
qKey.addEventListener( 'holding', function( event ) { cameraControls.truck( 0,   0.05 * event.deltaTime, false ) } );
eKey.addEventListener( 'holding', function( event ) { cameraControls.truck( 0, - 0.05 * event.deltaTime, false ) } );

var starQty = 500;
var starGemoetry = new THREE.BufferGeometry();
var startPositions = new Float32Array(starQty * 3);

for (var i = 0; i < starQty; i++) {
	var i3 = i * 3;
	startPositions[i3] = (Math.random()*200) - 100;
	startPositions[i3 + 1] = (Math.random()*200) - 100;
	startPositions[i3 + 2] = (Math.random()*200) - 100;
}

starGemoetry.setAttribute('position', new THREE.BufferAttribute(startPositions, 3));

var starMaterial = new THREE.PointsMaterial({
	size: 0.1,
	transparent: true,
	opacity: 0.7
});

var stars = new THREE.Points(starGemoetry, starMaterial);
scene.add(stars);

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let planets = [];
let orbitControls = [];
let repoObjects = [];

function getRandomColor() {
	var color = "";
	// 너무 어두우면 안되니 최소한 각 색상이 8 이상이 되도록 한다.
	for (var i = 0; i < 6; i++) {
		color += Math.floor(Math.random() * 10 + 13).toString(16);
	}
	return parseInt(color, 16);
}

fetch("http://43.202.167.77:8000/repo-category")
.then((response) => {
	if (!response.ok) {
		throw new Error('Network response was not ok');
	}
	return response.json();
})
.then((data) => {
	makeStarRoad(data);
})
.catch((error) => {
	console.error('There has been a problem with your fetch operation:', error);
});

function makeStarRoad(data) {

	var categories = [];
	var positions = [];
	var data_category = data["categories"];

	for (var i = 0; i < data_category.length; i++) {
		categories.push(data_category[i].category);
		positions.push(data_category[i].position);
	}

	for (var i = 0; i < categories.length; i++) {
		var color1 = getRandomColor();
		var color2 = getRandomColor();

		var sun_geometry = new THREE.SphereGeometry(5, 32, 16);
		var sun_material = new THREE.MeshStandardMaterial({ 
			color : 0xffffff,
			emissive: color1, // 발광 색상 설정
			emissiveIntensity: 5, // 발광 강도 설정
			transparent: true, // 투명하게 설정
			opacity: 0.5 // 투명도 설정 (0은 완전 투명, 1은 완전 불투명)
		});

		var sun_sphere = new THREE.Mesh(sun_geometry, sun_material);
		// var random_pos_x = Math.random() * 30 - 15;
		// var random_pos_y = Math.random() * 30 - 15;
		// var random_pos_z = Math.random() * 30 - 15;
		// positions[i] = [random_pos_x, random_pos_y, random_pos_z];

		sun_sphere.position.set(positions[i][0] * 5, positions[i][1] * 5, positions[i][2] * 5);
		sun_sphere.name = categories[i];
		scene.add(sun_sphere);
		planets.push(sun_sphere);
		orbitControls.push({"sun": categories[i], "position": positions[i]})

		
		// var sun_text = document.createElement('div');
		// sun_text.className = 'label';
		// sun_text.textContent = categories[i];
		// sun_text.style.color = 'black';
		// sun_text.style.fontSize = '14px';
		// // sun_text.style.backgroundColor = 'red';
		// var sun_label = new CSS2DObject(sun_text);
		// sun_label.position.set(positions[i][0] * 5, positions[i][1] * 5, positions[i][2] * 5);
		// scene.add(sun_label);

		const sphere1 = new THREE.SphereGeometry(2, 16, 8);
		const sphere2 = new THREE.SphereGeometry(2, 16, 8);

		// color를 랜덤한 2개의 값을 넣어준다.
		var light1 = new THREE.PointLight( color1, 1000);
		var light2 = new THREE.PointLight( color2, 1000);
		light1.position.set( positions[i][0] * 5 + 0.3, positions[i][1] * 5, positions[i][2] * 5);
		light2.position.set( positions[i][0] * 5, positions[i][1] * 5 + 0.3, positions[i][2] * 5);
		light1.add(new THREE.Mesh(sphere1, new THREE.MeshBasicMaterial({ color: color1, transparent: true, opacity: 0})));
		light2.add(new THREE.Mesh(sphere2, new THREE.MeshBasicMaterial({ color: color2, transparent: true, opacity: 0})));
		scene.add( light1 );
		scene.add( light2 );
	}

	let orbitSystem = new THREE.Group();
	var orbitRadius = 5;
	var data_repo_category = data["repo-category"];

    for (var i = 0; i < data_repo_category.length; i++) {
        var repo = data_repo_category[i].repo;
        var categories = data_repo_category[i].categories;
        var points = [];
		
        for (var j = 0; j < categories.length; j++) {
            orbitRadius += Math.random();
            var category = categories[j];

            var repo_position, category_position;
            for (var k = 0; k < orbitControls.length; k++) {
                if (orbitControls[k].moon == repo)
                    repo_position = orbitControls[k].position;
                if (orbitControls[k].sun == category)
                    category_position = orbitControls[k].position;
            }

            // 각 카테고리마다 다른 각도 오프셋 적용
            var angleOffset = Math.random() * Math.PI * 2;
            // 각 카테고리마다 다른 기울기 적용
            var tiltAngle = Math.random() * Math.PI * 2;
			
			const detail= 20
            for (var index = 0; index < detail; index++) {
                var angle = (index * Math.PI * 2 / detail) + angleOffset;
                var x = Math.cos(angle) * orbitRadius;
                var z = Math.sin(angle) * orbitRadius;

                // 기울기 적용
                var y = Math.sin(angle) * Math.sin(tiltAngle) * orbitRadius;
                x *= Math.cos(tiltAngle);

                var dotGeometry = new THREE.SphereGeometry(0.1, 32, 16);
                var dotMaterial = new THREE.MeshBasicMaterial({ color: 0xbdb3db });
                var dotMesh = new THREE.Mesh(dotGeometry, dotMaterial);
                dotMesh.position.set(
                    x + category_position[0] * 5,
                    y + category_position[1] * 5,
                    z + category_position[2] * 5
                );
                points.push(new THREE.Vector3(dotMesh.position.x, dotMesh.position.y, dotMesh.position.z));
            }
        }

        // Catmull-Rom Curve 생성
        var curve = new THREE.CatmullRomCurve3(points, true);
		var material = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 1 });

        var repoObject = {
            name: repo,
            curve: curve,
            parameter: 0, // curve 상의 현재 위치 (0 ~ 1)
            mesh: material
        };

		// repo를 표현할 3D 객체 생성
		var moonGeometry = new THREE.SphereGeometry(1, 32, 16);
		var moonMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
		repoObject.mesh = new THREE.Mesh(moonGeometry, moonMaterial);
		scene.add(repoObject.mesh);

		repoObjects.push(repoObject);

        // 점들로부터 geometry 생성
        var curvePoints = curve.getPoints(100);
        var geometry = new THREE.BufferGeometry().setFromPoints(curvePoints);

        // // Line material 생성
        var material = new THREE.LineBasicMaterial({ 
				color: 0xffffff, 
				// transparent: true, 
				// opacity: 0.3, 
				visible: false 
			});
        var curveObject = new THREE.Line(geometry, material);

        // orbitSystem에 추가
        orbitSystem.add(curveObject);
    }
	
	scene.add(orbitSystem);
}

function updateRepos() {
    repoObjects.forEach(repo => {
        repo.parameter = (repo.parameter + 0.0002) % 1; // 속도 조절 가능
        var position = repo.curve.getPointAt(repo.parameter);
        repo.mesh.position.copy(position);
    });
}

function onMouseClick(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(planets);
    if (intersects.length > 0) {
        const target = intersects[0].object.position;
        cameraControls.moveTo(target.x, target.y, target.z, true);
    }
}

function onMouseMove(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    
    const intersects = raycaster.intersectObjects(planets);
    if (intersects.length > 0) {
        const target = intersects[0].object;
		// console.log(target);
        const vector = new THREE.Vector3();
        vector.copy(target.position).project(camera);
        
        hoveredLabel.style.top = `${event.clientY - 15}px`;
		hoveredLabel.style.left = `${event.clientX + 50}px`;
		hoveredLabel.textContent = target.name;
		// 사이즈를 조절
        hoveredLabel.style.display = 'block';
    } else {
        hoveredLabel.style.display = 'none';
    }
}


renderer.domElement.addEventListener('click', onMouseClick, false);
renderer.domElement.addEventListener('mousemove', onMouseMove, false);

function animate() {
    const delta = clock.getDelta();
    const updated = cameraControls.update(delta);

    updateRepos();
    renderer.render(scene, camera);
    labelRenderer.render(scene, camera);
    requestAnimationFrame(animate);
}

animate();

function customFitTo() {
	const distanceToFit = cameraControls.getDistanceToFitBox( meshBBWidth, meshBBHeight, meshBBDepth );
	cameraControls.moveTo(
		mesh.position.x,
		mesh.position.y,
		mesh.position.z + distanceToFit,
		true
	);
	cameraControls.rotateTo( 0, 90 * THREE.MathUtils.DEG2RAD, true );

}

// make variable available to browser console
globalThis.THREE = THREE;
globalThis.CameraControls = CameraControls;
globalThis.camera = camera;
globalThis.cameraControls = cameraControls;
globalThis.customFitTo = customFitTo;



/**
핵심 코어 기능
1. library는 THREE.js (3D 라이브러리), CSS2DRenderer (2D 렌더러), hold-event (키보드 이벤트), camera-controls (카메라 컨트롤러)를 사용한다

2. 3D 랜더링을 필요한 필수 요소 : Scene, Camera, Renderer
	2-1. Scene : 3D 공간을 의미하며, 모든 객체들이 포함되는 공간이다
	2-2. Camera : 사용자가 보는 시점을 의미하며, 여러 종류가 있다. 여기서는 PerspectiveCamera를 사용한다
	2-3. Renderer : Scene과 Camera를 렌더링하여 화면에 표시하는 역할을 한다

3. 물체 생성
	3-1. SphereGeometry : 구체를 생성하는 객체이며, radius, widthSegments, heightSegments를 인자로 받는다
	3-2. MeshStandardMaterial : 물체의 속성을 정의하는 객체이며, color, emissive, emissiveIntensity, transparent, opacity를 인자로 받는다
	3-3. Mesh : 물체를 생성하는 객체이며, geometry, material를 인자로 받는다

4. WebGL Pipeline
	4-1. [Input geometry + Attributes]
	4-2. Memory (: Gemotry, Buffer, Texture 등이 저장되는 공간)
	4-3. JavaScript (: GPU에 전달되는 공간)
	4-3. Vertex Shader (: Vertex의 위치를 계산하는 공간)
	4-4. Primitive Assembly[= Triangle Assembly] (: Vertex를 삼각형으로 변환하는 공간)
	4-5. Rasterization (: 삼각형을 화면에 표시하는 공간)
	4-6. Fragment Shader (: 픽셀의 색상을 계산하는 공간)
	4-7. Fragment Operation (: 픽셀의 색상을 조작하는 공간)
	4-8. Frame Buffer (: 화면에 표시되는 공간)

**/ 
