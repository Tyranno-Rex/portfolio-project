package site.springboot.user.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import site.springboot.user.entities.User;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email); // 중복 가입 확인
}