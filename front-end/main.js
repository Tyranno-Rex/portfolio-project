import * as THREE from 'three';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import * as holdEvent from "https://unpkg.com/hold-event@0.2.0/dist/hold-event.module.js";
import CameraControls from './dist/camera-controls.module.js';
// marked.js를 사용하기 위해 import
CameraControls.install( { THREE: THREE } );

const width = window.innerWidth;
const height = window.innerHeight;
const clock = new THREE.Clock();
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 60, width / height, 0.01, 600);

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

var ClickedCategory = false;
var ClickedRepo = false;
var WindowChange = true;
var GameModeFlag = false;


const WhenStart = "2022-07-09";
var start = new Date(WhenStart);

function convertTime(milliseconds) {
    var seconds = Math.floor(milliseconds / 1000);
    var years = Math.floor(seconds / (365 * 24 * 3600));
    seconds -= years * (365 * 24 * 3600);
    var days = Math.floor(seconds / (24 * 3600));
    seconds -= days * (24 * 3600);
    var hours = Math.floor(seconds / 3600);
    seconds -= hours * 3600;
    var minutes = Math.floor(seconds / 60);
    seconds -= minutes * 60;

    return {
        years: years,
        days: days,
        hours: hours,
        minutes: minutes,
        seconds: seconds
    };
}

function updateCreditText() {
    var today = new Date();
    var diff = today.getTime() - start.getTime();
    var convertedTime = convertTime(diff);
    
    creditText.innerHTML = 
		'created by <a href="https://github.com/Tyranno-Rex"\
		target="_blank" style="color: white;">Tyranno-Rex</a>\
        <br>contact: jsilvercastle@gmail.com\
		<br>notion : <a href="https://uttermost-meteoroid-5fa.notion.site/c589ce11b68443e6ab545ad8879a6cc1">JSilverCastle\'s Notion</a>\
		<br>resume : <a href="https://uttermost-meteoroid-5fa.notion.site/b52bd3e5ca494049b06d6a9a9d19f846?pvs=4">JSilverCastle\'s Resume</a>\
        <br>From my first hello world : \
        ' + convertedTime.years + ' years ' + convertedTime.days + ' days \
        ' + convertedTime.hours + ' hours ' + convertedTime.minutes + ' minutes \
        ' + convertedTime.seconds + ' seconds'+
		'<br><br>' +
		'<br> Jesus answered, “I am the way and the truth and the life. No one comes to the Father except through me."'
		+ '<br> John 14:6';
}

let creditText = document.createElement('div');
creditText.className = 'credit';
creditText.style.color = 'white';
creditText.style.fontSize = '30px';
creditText.style.pointerEvents = 'auto';

let creditLabel1 = new CSS2DObject(creditText);
creditLabel1.position.set(-1000, 0, 0);
scene.add(creditLabel1);

labelRenderer.domElement.style.pointerEvents = 'none';
updateCreditText();
setInterval(updateCreditText, 1000);

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

var starQty = 3000;
var starGemoetry = new THREE.BufferGeometry();
var startPositions = new Float32Array(starQty * 3);

for (var i = 0; i < starQty; i++) {
	var i3 = i * 3;
	startPositions[i3] = (Math.random()*2000) - 1000;
	startPositions[i3 + 1] = (Math.random()*2000) - 1000;
	startPositions[i3 + 2] = (Math.random()*2000) - 1000;
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
let SelectedCategory = [];
var repoLabels = [];
var categoryLabels = [];
let orbitControls = [];
let repoObjects = [];
let repoAndCategory = [];
let orbitSystem = new THREE.Group();

function getRandomColor() {
	var color = "";
	// 너무 어두우면 안되니 최소한 각 색상이 8 이상이 되도록 한다.
	for (var i = 0; i < 6; i++) {
		color += Math.floor(Math.random() * 10 + 13).toString(16);
	}
	return parseInt(color, 16);
}

fetch("https://jeongeunseong.site:8000/repo-category")
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


// 1 RENDERING PROCESS
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
		// var number = 1;
		// var random_pos_x = Math.random() * number - number / 2;
		// var random_pos_y = Math.random() * number - number / 2;
		// var random_pos_z = Math.random() * number - number / 2;
		// positions[i] = [positions[i][0] + random_pos_x, positions[i][1] + random_pos_y, positions[i][2] + random_pos_z];

		sun_sphere.position.set(positions[i][0] * 5, positions[i][1] * 5, positions[i][2] * 5);
		sun_sphere.name = categories[i];
		scene.add(sun_sphere);
		planets.push(sun_sphere);
		orbitControls.push({"sun": categories[i], "position": positions[i]});

		const sphere1 = new THREE.SphereGeometry(2, 16, 8);
		const sphere2 = new THREE.SphereGeometry(2, 16, 8);

		// color를 랜덤한 2개의 값을 넣어준다.
		var light1 = new THREE.PointLight( color1, 2000);
		var light2 = new THREE.PointLight( color2, 2000);
		light1.position.set( positions[i][0] * 5 + 0.3, positions[i][1] * 5, positions[i][2] * 5);
		light2.position.set( positions[i][0] * 5, positions[i][1] * 5 + 0.3, positions[i][2] * 5);
		light1.add(new THREE.Mesh(sphere1, new THREE.MeshBasicMaterial({ color: color1, transparent: true, opacity: 0})));
		light2.add(new THREE.Mesh(sphere2, new THREE.MeshBasicMaterial({ color: color2, transparent: true, opacity: 0})));
		scene.add( light1 );
		scene.add( light2 );
	}

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
            // var angleOffset = 0;
            // 각 카테고리마다 다른 기울기 적용
            var tiltAngle = Math.random() * Math.PI * 2;
			
			const detail= 10
            for (var index = 0; index < detail; index++) {
                var angle = (index * Math.PI * 2 / detail) + angleOffset;
                // var angle = (index * Math.PI * 2 / detail);
                var x = Math.cos(angle) * orbitRadius;
                var z = Math.sin(angle) * orbitRadius;

                // 기울기 적용
                var y = Math.sin(angle) * Math.sin(tiltAngle) * orbitRadius;

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
            mesh: material,
			namevisible: false
        };

		// repo를 표현할 3D 객체 생성
		var moonGeometry = new THREE.SphereGeometry(1, 32, 16);
		var moonMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
		repoObject.mesh = new THREE.Mesh(moonGeometry, moonMaterial);
		repoObject.mesh.name = repo;
		scene.add(repoObject.mesh);

		repoObjects.push(repoObject);
		repoAndCategory.push({repo: repo, categories: categories});
        // 점들로부터 geometry 생성
        var curvePoints = curve.getPoints(100);
        var geometry = new THREE.BufferGeometry().setFromPoints(curvePoints);

        // // Line material 생성
        var material = new THREE.LineBasicMaterial({ 
				name: repo,
				color: 0xffffff, 
				transparent: true, 
				opacity: 0.3, 
				visible: false 
			});
        var curveObject = new THREE.Line(geometry, material);

        // orbitSystem에 추가
        orbitSystem.add(curveObject);
    }
	
	scene.add(orbitSystem);

	var repoNameList = "";

	for (var i = 0; i < repoObjects.length; i++) {
		repoNameList += "<div class='repo-indicator' onclick='ShowRepoFunc(\"" + repoObjects[i].name + "\")'>" + repoObjects[i].name + "</div>";
	}
	document.getElementsByClassName('repo-indicator-container')[0].innerHTML = repoNameList;
	
}

// function updateRepos() {
	
// 	categoryLabels.forEach(label => {
// 		scene.remove(label);
// 	});
// 	categoryLabels = [];
// 	SelectedCategory.forEach(category => {
// 		planets.forEach(planet => {
// 			if (planet.name == category) {
// 				var vector = new THREE.Vector3();
// 				vector.copy(planet.position).project(camera);
// 				var div = document.createElement('div');
// 				div.className = 'label';
// 				div.textContent = category;
// 				div.style.color = 'white';
// 				div.style.fontSize = '20px';
// 				div.style.fontFamily = 'SoDoSans';
// 				var label = new CSS2DObject(div);
// 				label.position.set(planet.position.x, planet.position.y, planet.position.z);
// 				scene.add(label);
// 				categoryLabels.push(label);
// 			}
// 		});
// 	});
//     repoLabels.forEach(label => {
//         scene.remove(label);
//     });
//     repoLabels = []; 
//     repoObjects.forEach(repo => {
//         repo.parameter = (repo.parameter + 0.0001) % 1; // 속도 조절 가능
//         var position = repo.curve.getPointAt(repo.parameter);
//         repo.mesh.position.copy(position);
//         if (repo.namevisible == true) {
//             var vector = new THREE.Vector3();
//             vector.copy(position).project(camera);
//             var div = document.createElement('div');
//             div.className = 'label';
//             div.textContent = repo.name;
//             div.style.color = 'white';
//             div.style.fontSize = '10px';
// 			div.style.fontFamily = 'SoDoSans';
//             var label = new CSS2DObject(div);
//             label.position.set(position.x + 3, position.y + 3, position.z + 3);
//             scene.add(label);
//             repoLabels.push(label); // 배열에 라벨 추가
//         }    
//     });
// }

function updateRepos(delta) {
    categoryLabels.forEach(label => {
        scene.remove(label);
    });
    categoryLabels = [];
    SelectedCategory.forEach(category => {
        planets.forEach(planet => {
            if (planet.name == category) {
                var vector = new THREE.Vector3();
                vector.copy(planet.position).project(camera);
                var div = document.createElement('div');
                div.className = 'label';
                div.textContent = category;
                div.style.color = 'white';
                div.style.fontSize = '20px';
                div.style.fontFamily = 'SoDoSans';
                var label = new CSS2DObject(div);
                label.position.set(planet.position.x, planet.position.y, planet.position.z);
                scene.add(label);
                categoryLabels.push(label);
            }
        });
    });
    repoLabels.forEach(label => {
        scene.remove(label);
    });
    repoLabels = [];
    repoObjects.forEach(repo => {
        repo.parameter = (repo.parameter + delta * 0.01) % 1; // delta 값을 곱하여 프레임 속도에 독립적인 속도로 회전합니다.
        var position = repo.curve.getPointAt(repo.parameter);
        repo.mesh.position.copy(position);
        if (repo.namevisible == true) {
            var vector = new THREE.Vector3();
            vector.copy(position).project(camera);
            var div = document.createElement('div');
            div.className = 'label';
            div.textContent = repo.name;
            div.style.color = 'white';
            div.style.fontSize = '10px';
            div.style.fontFamily = 'SoDoSans';
            var label = new CSS2DObject(div);
            label.position.set(position.x + 3, position.y + 3, position.z + 3);
            scene.add(label);
            repoLabels.push(label); // 배열에 라벨 추가
        }    
    });
}

function ShowRepoFunc(repo_name) {
	repoObjects.forEach(repo => {
		if (repo.mesh.name == repo_name) {
			repo.mesh.visible = true;
		} else {
			repo.mesh.visible = false;
		}
	});

	// 해당 repo의 궤도를 보여준다.
	orbitSystem.children.forEach(orbit => {
		if (orbit.material.name == repo_name) {
			orbit.material.visible = true;
		} else {
			orbit.material.visible = false;
		}
	});

	// 해당 repo와 연결된 category들을 보여준다.
	var repo = repo_name;
	orbitControls.forEach(orbitControl => {
		if (repoAndCategory.find(x => x.repo == repo).categories.includes(orbitControl.sun)) {
			scene.getObjectByName(orbitControl.sun).visible = true;
			SelectedCategory.push(orbitControl.sun);
		} else {
			scene.getObjectByName(orbitControl.sun).visible = false;
		}
	});
	
	// fetch("http://192.168.3.3:8000/get-repo-info?repo=" + repo)
	fetch("https://jeongeunseong.site:8000/get-repo-info?repo=" + repo)
	.then((response) => {
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json();
	})
	.then((data) => {
		var get_name = data.name;
		// var get_url = data.url; 양 끝에 ''를 제거
		var get_url = data.url.slice(8, -1);
		var get_readme = data.readme;
		var get_description = data.description;
		var get_complete_status = data.complete_status;
		var get_multi = data.multi;
		var get_subproject = data.subproject;
		const modalContent = `
			<div class="detail-title">Information about ${repo}</div><br>
			<div class="detail-name">Name: ${get_name}</div><br>
			<div class="detail-url">URL: <a href=https://${get_url} target="_blank">https:/${get_url}</a></div><br>
			<div class="detail-description">Description: ${get_description}</div><br>
			<div class="detail-complete-status">Complete Status: ${get_complete_status}</div><br>
			<div class="detail-multi">Multi: ${get_multi}</div><br>
			<div class="detail-subproject">Subproject: ${get_subproject}</div><br>
		`;
		document.getElementById('modal-content').innerHTML = modalContent;
		const readme = `<div class="detail-readme">${get_readme}</div><br>`;
		const htmlReadme = marked.parse(readme);
		document.getElementById('modal-content').innerHTML += htmlReadme;
	})
	.catch((error) => {
		console.error('There has been a problem with your fetch operation:', error);
	});
	
	myModal.open('#myModal');

	const target = repoObjects.find(x => x.name == repo_name).mesh.position;
	cameraControls.moveTo(target.x, target.y, target.z, true);

	showRepoName(repo_name);
}

// 2. MOUSE EVENT
function onMouseClick(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(planets);
    
	// Category를 클릭했을 때
	if (intersects.length > 0) {
		ResetClick(true, false);

		WindowChange = true;

		const target = intersects[0].object.position;
        cameraControls.moveTo(target.x, target.y, target.z, true);

		// 그리고 해당 category에 해당하는 repo들을 보여주고, 다른 repo들은 숨긴다.
		var category = intersects[0].object.name;
		repoObjects.forEach(repo => {
			if (repoAndCategory.find(x => x.repo == repo.name).categories.includes(category)) {
				repo.mesh.visible = true;
			} else {
				repo.mesh.visible = false;
			}
		});

		// 그리고 해당 category에 해당하는 sun을 보여주고, 다른 sun들은 숨긴다.
		orbitControls.forEach(orbitControl => {
			if (orbitControl.sun == category) {
				scene.getObjectByName(orbitControl.sun).visible = true;
			}
			else {
				scene.getObjectByName(orbitControl.sun).visible = false;
			}
		});

		// 그리고 모든 궤도를 숨긴다.
		orbitSystem.children.forEach(orbit => {
			orbit.material.visible = false;
		});
		
		SelectedCategory = [];
		SelectedCategory.push(category);
		SliderDisplayChange(false);
		showRepoNameWithCategory(intersects[0].object.name);
	}

	// Repo를 클릭했을 때
	const intersects2 = raycaster.intersectObjects(repoObjects.map(repo => repo.mesh));
	if (intersects2.length > 0) {
		ResetClick(false, true);
		WindowChange = true;
		// 해당 repo가 아닌 다른 repo들을 숨긴다.

		ShowRepoFunc(intersects2[0].object.name);
		SliderDisplayChange(false);
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

function MoveToSun(suntitle) {
	for (var i = 0; i < planets.length; i++) {
		if (planets[i].name == suntitle) {
			planets[i].visible = true;
			// cameraControls.moveTo(planets[i].position.x, planets[i].position.y, planets[i].position.z, true);
		} else {
			planets[i].visible = false;
		}

		for (var j = 0; j < repoObjects.length; j++) {
			if (repoAndCategory.find(x => x.repo == repoObjects[j].name).categories.includes(suntitle)) {
				repoObjects[j].mesh.visible = true;
			} else {
				repoObjects[j].mesh.visible = false;
			}
		}
	}
}

function SliderDisplayChange(flag) {
	var slider1 = document.getElementsByClassName('slider');
	var slider2 = document.getElementsByClassName('slider2');
	for (var i = 0; i < slider1.length; i++) {
		if (flag) {
			slider1[i].style.display = 'flex';
			slider2[i].style.display = 'flex';
		} else {
			slider1[i].style.display = 'none';
			slider2[i].style.display = 'none';
		}
	}
}

function showCategoryDetail(category) {
	ResetClick(true, false);
	MoveToSun(category);
	SliderDisplayChange(false);
	showRepoNameWithCategory(category);
	SelectedCategory.push(category);
}

function showRepoName(repo) {
	for (var i = 0; i < repoObjects.length; i++) {
		if (repoObjects[i].name == repo) {
			repoObjects[i].namevisible = true;
		} 
	}
}

function showRepoNameWithCategory(category) {
	for (var i = 0; i < repoObjects.length; i++) {
		if (repoAndCategory.find(x => x.repo == repoObjects[i].name).categories.includes(category)) {
			repoObjects[i].namevisible = true;
		} 
	}

}

// 3. UTIL FUNCTION
function ResetClick(category_flag, repo_flag) {
	if (category_flag == true)
		ClickedCategory = true;
	if (repo_flag == true)
		ClickedRepo = true;
	if (category_flag == false)
		ClickedCategory = false;
	if (repo_flag == false)
		ClickedRepo = false;
	

	// 모든 repo의 namevisible을 false로 바꾼다.
	for (var i = 0; i < repoObjects.length; i++) {
		repoObjects[i].namevisible = false;
	}
}

let spheres = []; // 공들
let GamePoint = 0; // 게임 점수
let GameLimitTime = 30; // 게임 제한 시간

function createSphere(startPoint, direction) {
    var geometry = new THREE.SphereGeometry(2, 32, 32);
    var material = new THREE.MeshBasicMaterial({ color: 0xffffff });
    var sphere = new THREE.Mesh(geometry, material);
    sphere.position.copy(startPoint);
    sphere.userData.direction = direction;
    sphere.userData.speed = 500; // 공의 속도 설정
    spheres.push(sphere);
    scene.add(sphere);
}

function moveSpheres(delta) {
    for (let i = spheres.length - 1; i >= 0; i--) {
        let sphere = spheres[i];
        sphere.position.add(sphere.userData.direction.clone().multiplyScalar(sphere.userData.speed * delta));
		

		// 카테고리나 레포와 충돌했을 때 -> 카테고리와 레포를 삭제하고, 공을 삭제한다.
		for (var j = 0; j < planets.length; j++) {
			if (sphere.position.distanceTo(planets[j].position) < 5) {
				scene.remove(planets[j]);
				planets.splice(j, 1);
				scene.remove(sphere);
				spheres.splice(i, 1);
				GamePoint += 10;
				document.getElementsByClassName('GameModePoint')[0].innerHTML = "POINT: " + GamePoint;
			}
		}

		for (var j = 0; j < repoObjects.length; j++) {
			if (sphere.position.distanceTo(repoObjects[j].mesh.position) < 5) {
				scene.remove(repoObjects[j].mesh);
				repoObjects.splice(j, 1);
				scene.remove(sphere);
				spheres.splice(i, 1);
				GamePoint += 1;
				document.getElementsByClassName('GameModePoint')[0].innerHTML = "POINT: " + GamePoint;
			}
		}


        // 공이 일정 거리를 벗어나면 제거
        if (sphere.position.distanceTo(camera.position) > 2000) {
            scene.remove(sphere);
            spheres.splice(i, 1);
        }
    }
}

function onMouseClick2(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);

	var startPoint = camera.position.clone().add(raycaster.ray.direction.clone().multiplyScalar(30));
    var direction = raycaster.ray.direction.clone().normalize();
    createSphere(startPoint, direction);
}

function GameModeUIDisplayChange() {
    const showChatButton = document.getElementById('showChatButton');
	const chatBubble = document.getElementById('chatBubble');
	const indicatorContent = document.getElementById('showIndicatorButton');
	const commandButton = document.getElementsByClassName('commands')[0];
	const title = document.getElementsByClassName('title')[0];
	const GameUI = document.getElementById('GameUI');
	
	if (GameModeFlag) {
		showChatButton.style.display = 'none';
		chatBubble.style.display = 'none';
		indicatorContent.style.display = 'none';
		commandButton.style.display = 'none';
		title.style.display = 'none';
		GameUI.style.display = 'block';
		renderer.domElement.style.cursor = 'crosshair';
	} else {
		showChatButton.style.display = 'block';
		chatBubble.style.display = 'block';
		indicatorContent.style.display = 'block';
		commandButton.style.display = 'block';
		title.style.display = 'block';
		GameUI.style.display = 'none';
		SliderDisplayChange(true);
		renderer.domElement.style.cursor = 'auto';
	}

}

// 4. GAME MODE
function GameMode() {
	GamePoint = 0;
	GameLimitTime = 30;
	GameModeFlag = !GameModeFlag;
	ResetClick(false, false);
	SliderDisplayChange(false);
	GameModeUIDisplayChange();
	renderer.domElement.removeEventListener('click', onMouseClick, false);
	renderer.domElement.removeEventListener('mousemove', onMouseMove, false);
	renderer.domElement.addEventListener('click', onMouseClick2, false);
}

renderer.domElement.addEventListener('click', onMouseClick, false);
renderer.domElement.addEventListener('mousemove', onMouseMove, false);


function animate() {
    const delta = clock.getDelta();
    const updated = cameraControls.update(delta);
	if (GameModeFlag) {
		if (GameLimitTime <= 0) {
			GameModeFlag = false;
			GameModeUIDisplayChange();
			alert("Game Over! Your Point is " + GamePoint);
			location.reload(true);
		}
		GameLimitTime -= delta;
		document.getElementsByClassName('GameModeTime')[0].innerHTML = "TIME: " + Math.floor(GameLimitTime);
		moveSpheres(delta);	
	}
    updateRepos(delta);
	renderer.render(scene, camera);
    labelRenderer.render(scene, camera);
    requestAnimationFrame(animate);
}

function showAll() {
	ResetClick(false, false);
	WindowChange = true;
	repoObjects.forEach(repo => {
		repo.mesh.visible = true;
	});
	orbitControls.forEach(orbitControl => {
		scene.getObjectByName(orbitControl.sun).visible = true;
	});
	orbitSystem.children.forEach(orbit => {
		orbit.material.visible = false;
	});
	SelectedCategory = [];
	SliderDisplayChange(true);
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

globalThis.THREE = THREE;
globalThis.CameraControls = CameraControls;
globalThis.camera = camera;
globalThis.cameraControls = cameraControls;
globalThis.customFitTo = customFitTo;
window.showAll = showAll;
window.showCategoryDetail = showCategoryDetail;
window.ShowRepoFunc = ShowRepoFunc;
window.GameMode = GameMode;
export { showAll };