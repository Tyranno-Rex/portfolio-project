(function() {
    'use strict';
    var scene, camera, renderer;

    var container, aspectRatio, HEIGHT, WIDTH, 
    fieldOfView, nearPlane, farPlane, mouseX, mouseY,
    windowHalfX, windowHalfY, stats, geometry, starStuff,
    materialOptions, stars, mouseWheel, earthGroup;

    init();
    animate();

    function init() {
        container = document.createElement('div');
        document.body.appendChild(container);
        document.body.style.overflow = 'hidden';

        HEIGHT = window.innerHeight;
        WIDTH = window.innerWidth;
        aspectRatio = WIDTH / HEIGHT;
        fieldOfView = 75;
        nearPlane = 1;
        farPlane = 1000;
        mouseX = 0;
        mouseY = 0;
        mouseWheel = 0;
        windowHalfX = WIDTH / 2;
        windowHalfY = HEIGHT / 2;

        camera = new THREE.PerspectiveCamera(
            fieldOfView,
            aspectRatio,
            nearPlane,
            farPlane
        );

        camera.position.z = farPlane / 2;
        scene = new THREE.Scene({ antialias: true });
        scene.fog = new THREE.FogExp2(0x000000, 0.0003);

        starForge();

        if (webGLSupport()) {
            renderer = new THREE.WebGLRenderer({alpha: true});
        } else {
            renderer = new THREE.CanvasRenderer();
        }

        renderer.setClearColor(0x000011, 1);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(WIDTH, HEIGHT);
        container.appendChild(renderer.domElement);

        stats = new Stats();
        stats.domElement.style.position = 'absolute';
        stats.domElement.style.top = '0px';
        stats.domElement.style.right = '0px';
        container.appendChild(stats.domElement);


        window.addEventListener('resize', onWindowResize, false);
        document.addEventListener('mousemove', onMouseMove, false);
        document.addEventListener('wheel', onMouseWheel, false);
    }

    function animate() {
        requestAnimationFrame(animate);
        render();
        stats.update();
    }

    function render() {
        camera.position.x += (mouseX - camera.position.x) * 0.005;
        camera.position.y += (mouseY - camera.position.y) * 0.005;
        camera.position.z += (mouseWheel - camera.position.z) * 0.05;
        // earthGroup.rotation.y += 0.01;
        camera.lookAt(scene.position);
        renderer.render(scene, camera);
    }

    function webGLSupport() {
        try {
            var canvas = document.createElement('canvas');
            return !!(window.WebGLRenderingContext && 
            (canvas.getContext('webgl') || 
            canvas.getContext('experimental-webgl')));
        } catch (e) {
            return false;
        }
    }

    function onWindowResize() {
        var HEIGHT = window.innerHeight;
            WIDTH = window.innerWidth;
        
            camera.aspect = aspectRatio;
            camara.updateProjectionMatrix();
            renderer.setSize(WIDTH, HEIGHT);
    }

    function starForge() {
        var starQty = 10000;
        geometry = new THREE.SphereGeometry(1000, 32, 16);
        
        materialOptions = {
            size : 0.1,
            transparent: true,
            opacity: 0.7
        };
        
        starStuff = new THREE.PointCloudMaterial(materialOptions);
        
        for (var i = 0; i < starQty; i++) {
            var starVertex = new THREE.Vector3();
            starVertex.x = Math.random() * 2000 - 1000;
            starVertex.y = Math.random() * 2000 - 1000;
            starVertex.z = Math.random() * 2000 - 1000;
            
            geometry.vertices.push(starVertex);
        }
        
        stars = new THREE.PointCloud(geometry, starStuff);
        scene.add(stars);



        
        
        
        
        // // 태양 생성
        // var sunGeometry = new THREE.SphereGeometry(50, 32, 32);  // 적절한 크기로 설정
        // var sunMaterial = new THREE.MeshBasicMaterial({ 
        //     color: 0xff0000, 
        //     transparent: true,
        //     opacity: 1
        // });
        
        // var sun = new THREE.Mesh(sunGeometry, sunMaterial);
        // sun.position.set(0, 0, 0);  // 태양의 위치를 중앙으로 설정
        
        
        // var sunLight = new THREE.PointLight(0xffffff, 1.5, 1000, 2);
        // sunLight.position.set(0, 0, 0);
        // scene.add(sunLight);


        
        
        
        
        // // 지구 생성
        // var earthGeometry = new THREE.SphereGeometry(10, 32, 32);  // 적절한 크기로 설정
        // var earthMaterial = new THREE.MeshBasicMaterial({ 
        //     color: 0x0000ff, 
        //     transparent: true,
        //     opacity: 1
        // });
        
        
        // var earth = new THREE.Mesh(earthGeometry, earthMaterial);
        // earthGroup = new THREE.Group();
        // earth.position.set(200, 0, 0);  // 지구의 위치를 태양에서 200만큼 떨어진 위치로 설정
        // earthGroup.add(sun);
        // earthGroup.add(earth);
        // scene.add(earthGroup);

        // // 흰색 선 생성
        // var lineGeometry = new THREE.Geometry();
        // lineGeometry.vertices.push(
        //     new THREE.Vector3(0, 0, 0),  // 태양의 위치 (0, 0, 0)
        //     earth.position.clone()      // 지구의 위치
        // );

        // var lineMaterial = new THREE.LineBasicMaterial({ color: 0xffffff });
        // var line = new THREE.Line(lineGeometry, lineMaterial);
        // scene.add(line);


        // // 지구의 위치로부터 태양을 향하는 포인트 라이트 생성
        // var sunLight = new THREE.PointLight(0xffffff, 1, 200);
        // sunLight.position.copy(earth.position);
        // scene.add(sunLight);
    }
    
    function onMouseMove(e) {
        mouseX = e.clientX - windowHalfX;
        mouseY = e.clientY - windowHalfY;
    }
    
    function onMouseWheel(e) {
        mouseWheel += e.deltaY * 0.05; // Adjust the sensitivity as necessary
    }

}) ();