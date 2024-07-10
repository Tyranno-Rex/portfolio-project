let orbitSystem = new THREE.Group();

function handleData3(response_data) {
    const orbitRadius = 5; // 궤도의 반지름 (필요에 따라 조절)

    for (let i = 0; i < response_data.length; i++) {
        const repo = response_data[i].repo;
        const categories = response_data[i].categories;

        if (categories.length > 0) {
            const firstCategory = categories[0];
            let category_position;

            // 첫 번째 카테고리의 위치 찾기
            for (let k = 0; k < orbitControls.length; k++) {
                if (orbitControls[k].sun == firstCategory) {
                    category_position = orbitControls[k].position;
                    break;
                }
            }

            if (!category_position) continue; // 카테고리를 찾지 못한 경우 건너뛰기

            // repo를 위한 랜덤한 궤도 위치 생성
            const angle = Math.random() * Math.PI * 2;
            const x = Math.cos(angle) * orbitRadius;
            const z = Math.sin(angle) * orbitRadius;
            const y = (Math.random() - 0.5) * orbitRadius; // y축 변화를 위해

            const repoOrbitPosition = new THREE.Vector3(
                category_position[0] + x,
                category_position[1] + y,
                category_position[2] + z
            );

            // 궤도 생성
            const curve = new THREE.EllipseCurve(
                category_position[0], category_position[2], // 중심 x, z
                orbitRadius, orbitRadius, // x, z 반지름
                0, 2 * Math.PI, // 시작 각도, 종료 각도
                false, // 시계 방향
                0 // 회전
            );

            const points = curve.getPoints(50);
            const geometry = new THREE.BufferGeometry().setFromPoints(
                points.map(p => new THREE.Vector3(p.x, category_position[1], p.y))
            );
            const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
            const curveObject = new THREE.Line(geometry, material);

            orbitSystem.add(curveObject);

            // 여기에 repo 객체를 생성하고 repoOrbitPosition에 배치하는 코드를 추가할 수 있습니다.
            // 예: createRepoObject(repo, repoOrbitPosition);
        }
    }

    scene.add(orbitSystem);
}