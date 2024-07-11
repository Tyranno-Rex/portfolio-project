(function() {
    'use strict';
    var scene, camera, renderer, labelRenderer;

    var container, aspectRatio, HEIGHT, WIDTH, 
    fieldOfView, nearPlane, farPlane, mouseX, mouseY,
    windowHalfX, windowHalfY, stats, stars, mouseWheel;

    init();
    animate();

    function init() {
        container = document.createElement('div');
        document.body.appendChild(container);

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
        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x000000, 0.0003);

        starForge();

        if (webGLSupport()) {
            renderer = new THREE.WebGLRenderer({ alpha: true });
        } else {
            renderer = new THREE.CanvasRenderer();
        }

        renderer.setClearColor(0x000011, 1);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(WIDTH, HEIGHT);
        container.appendChild(renderer.domElement);

        labelRenderer = new THREE.CSS2DRenderer();
        labelRenderer.setSize(WIDTH, HEIGHT);
        labelRenderer.domElement.style.position = 'absolute';
        labelRenderer.domElement.style.top = '0px';
        container.appendChild(labelRenderer.domElement);

        stats = new Stats();
        stats.domElement.style.position = 'absolute';
        stats.domElement.style.top = '0px';
        stats.domElement.style.right = '0px';
        container.appendChild(stats.domElement);

        window.addEventListener('resize', onWindowResize, false);
        document.addEventListener('mousemove', onMouseMove, false);
        document.addEventListener('mousedown', onMouseDown, false);
        document.addEventListener('mouseup', onMouseUp, false);
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
        camera.lookAt(scene.position);
        renderer.render(scene, camera);
        labelRenderer.render(scene, camera);
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
        HEIGHT = window.innerHeight;
        WIDTH = window.innerWidth;

        camera.aspect = WIDTH / HEIGHT;
        camera.updateProjectionMatrix();
        renderer.setSize(WIDTH, HEIGHT);
        labelRenderer.setSize(WIDTH, HEIGHT);
    }

    function starForge() {
        var starQty = 10000;
        var geometry = new THREE.BufferGeometry();
        var positions = new Float32Array(starQty * 3);

        for (var i = 0; i < starQty; i++) {
            positions[i * 3] = Math.random() * 2000 - 1000;
            positions[i * 3 + 1] = Math.random() * 2000 - 1000;
            positions[i * 3 + 2] = Math.random() * 2000 - 1000;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        var materialOptions = {
            size: 0.1,
            transparent: true,
            opacity: 0.7
        };

        var starStuff = new THREE.PointsMaterial(materialOptions);
        stars = new THREE.Points(geometry, starStuff);
        scene.add(stars);

        // fetch 요청
        fetch("http://localhost:8000/repos")
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            handleData(data);
        })
        .catch((error) => {
            console.error('There has been a problem with your fetch operation:', error);
        });

        function handleData(response_data) {
            var repos = [];
            var positions = [];

            for (var i = 0; i < response_data.length; i++) {
                repos.push(response_data[i].repo);
                positions.push(response_data[i].position);
            }

            for (var i = 0; i < repos.length; i++) {
                var moon_geometry = new THREE.SphereGeometry(5, 32, 16);
                var moon_material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
                var moon_sphere = new THREE.Mesh(moon_geometry, moon_material);

                moon_sphere.position.set(positions[i][0] * 10, positions[i][1] * 10, positions[i][2] * 10);
                scene.add(moon_sphere);

                var moon_text = document.createElement('div');
                moon_text.className = 'label';
                moon_text.textContent = repos[i];
                var moon_label = new THREE.CSS2DObject(moon_text);
                moon_label.position.set(positions[i][0] * 10, positions[i][1] * 10, positions[i][2] * 10);
                scene.add(moon_label);
            }
        }


        fetch("http://localhost:8000/categories")
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            handleData2(data);
        })
        .catch((error) => {
            console.error('There has been a problem with your fetch operation:', error);
        });

        function handleData2(response_data) {
            var categories = [];
            var positions = [];
            
            for (var i = 0; i < response_data.length; i++) {
                categories.push(response_data[i].category);
                positions.push(response_data[i].position);
            }
            console.log(categories.length);

            for (var i = 0; i < categories.length; i++) {
                var moon_geometry = new THREE.SphereGeometry(10, 32, 16);
                var moon_material = new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe: true });
                var moon_sphere = new THREE.Mesh(moon_geometry, moon_material);

                

                moon_sphere.position.set(positions[i][0] * 10, positions[i][1] * 10, positions[i][2] * 10);
                scene.add(moon_sphere);

                var moon_text = document.createElement('div');
                moon_text.className = 'label';
                moon_text.textContent = categories[i];
                var moon_label = new THREE.CSS2DObject(moon_text);
                moon_label.position.set(positions[i][0] * 10, positions[i][1] * 10, positions[i][2] * 10);
                scene.add(moon_label);
            }
        }


    }

    // function onMouseMove(e) {
    //     mouseX = e.clientX - windowHalfX;
    //     mouseY = e.clientY - windowHalfY;
    // }

    function onMouseWheel(e) {
        mouseWheel += e.deltaY * 0.05; // Adjust the sensitivity as necessary
    }



    // let mouseX = 0, mouseY = 0;
    // let windowHalfX = window.innerWidth / 2;
    // let windowHalfY = window.innerHeight / 2;
    let isMouseDown = false;
    let startX = 0, startY = 0;
    let deltaX = 0, deltaY = 0;

    // 마우스 이동 이벤트 핸들러
    function onMouseMove(e) {
        if (isMouseDown) {
            mouseX = e.clientX - startX;
            mouseY = e.clientY - startY;
            // deltaX = e.clientX - startX;
            // deltaY = e.clientY - startY;
            // 화면을 전환할 때 사용할 로직을 여기에 추가합니다.
            // 예: 화면을 이동시키거나 특정 요소를 움직이는 등의 동작
            // console.log('Moving screen:', deltaX, deltaY);
            // 예: 화면 전환 효과 적용
            // document.body.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        }
    }

    // 마우스 다운 이벤트 핸들러
    function onMouseDown(e) {
        isMouseDown = true;
        startX = e.clientX;
        startY = e.clientY;
    }

    // 마우스 업 이벤트 핸들러
    function onMouseUp(e) {
        isMouseDown = false;
        // 화면 이동 완료 후 초기화
        // deltaX = 0;
        // deltaY = 0;
        startX = 0;
        startY = 0;

        document.body.style.transform = 'none';
    }
})();