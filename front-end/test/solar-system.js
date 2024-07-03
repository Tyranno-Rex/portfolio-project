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

        // 태양 생성
        var sunGeometry = new THREE.SphereGeometry(100, 32, 32);  // 적절한 크기로 설정
        var sunMaterial = new THREE.MeshBasicMaterial({ 
            color: 0xff0000, 
            transparent: true,
            opacity: 1
        });
        
        var sun = new THREE.Mesh(sunGeometry, sunMaterial);
        sun.position.set(0, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(sun);

        
        var mercuryGeometry = new THREE.SphereGeometry(0.7, 32, 32);  // 적절한 크기로 설정
        var mercuryMaterial = new THREE.MeshBasicMaterial({ 
            color: 0xC0C0C0,
            transparent: true,
            opacity: 1
        });
        
        var mercury = new THREE.Mesh(mercuryGeometry, mercuryMaterial);
        mercury.position.set(120, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(mercury);


        var venusGeometry = new THREE.SphereGeometry(1.6, 32, 32);  // 적절한 크기로 설정

        var venusMaterial = new THREE.MeshBasicMaterial({
            color: 0xCC9966,
            transparent: true,
            opacity: 1
        });

        var venus = new THREE.Mesh(venusGeometry, venusMaterial);
        venus.position.set(150, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(venus);


        var earthGeometry = new THREE.SphereGeometry(1.8, 32, 32);  // 적절한 크기로 설정
        var earthMaterial = new THREE.MeshBasicMaterial({ 
            color: 0x0080FF,
            transparent: true,
            opacity: 1
        });

        var earth = new THREE.Mesh(earthGeometry, earthMaterial);
        earth.position.set(200, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(earth);


        var marsGeometry = new THREE.SphereGeometry(1, 32, 32);  // 적절한 크기로 설정
        var marsMaterial = new THREE.MeshBasicMaterial({ 
            color: 0xCC3300, 
            transparent: true,
            opacity: 1
        });

        var mars = new THREE.Mesh(marsGeometry, marsMaterial);
        mars.position.set(240, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(mars);


        var jupiterGeometry = new THREE.SphereGeometry(20, 32, 32);  // 적절한 크기로 설정
        var jupiterMaterial = new THREE.MeshBasicMaterial({ 
            color: 0xFFFFFF, 
            transparent: true,
            opacity: 1
        });

        var jupiter = new THREE.Mesh(jupiterGeometry, jupiterMaterial);
        jupiter.position.set(300, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(jupiter);


        var saturnGeometry = new THREE.SphereGeometry(16, 32, 32);  // 적절한 크기로 설정
        var saturnMaterial = new THREE.MeshBasicMaterial({ 
            color: 0xFFFF99, 
            transparent: true,
            opacity: 1
        });

        var saturn = new THREE.Mesh(saturnGeometry, saturnMaterial);
        saturn.position.set(400, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(saturn);


        var uranusGeometry = new THREE.SphereGeometry(15, 32, 32);  // 적절한 크기로 설정
        var uranusMaterial = new THREE.MeshBasicMaterial({ 
            color: 0x66CCCC, 
            transparent: true,
            opacity: 1
        });

        var uranus = new THREE.Mesh(uranusGeometry, uranusMaterial);
        uranus.position.set(600, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(uranus);


        var neptuneGeometry = new THREE.SphereGeometry(15, 32, 32);  // 적절한 크기로 설정
        var neptuneMaterial = new THREE.MeshBasicMaterial({ 
            color: 0x0066CC, 
            transparent: true,
            opacity: 1
        });


        var neptune = new THREE.Mesh(neptuneGeometry, neptuneMaterial);
        neptune.position.set(4497, 0, 0);  // 태양의 위치를 중앙으로 설정
        scene.add(neptune);
    }
    
    function onMouseMove(e) {
        mouseX = e.clientX - windowHalfX;
        mouseY = e.clientY - windowHalfY;
    }
    
    function onMouseWheel(e) {
        mouseWheel += e.deltaY * 0.05; // Adjust the sensitivity as necessary
    }

}) ();