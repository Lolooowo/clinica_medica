
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


CREATE SCHEMA IF NOT EXISTS `clinica_medica` DEFAULT CHARACTER SET utf8mb4 ;
USE `clinica_medica` ;

-- -----------------------------------------------------
-- Table `clinica_medica`.`paciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`paciente` (
  `id_paciente` INT NOT NULL AUTO_INCREMENT,
  `nombres` VARCHAR(100) NOT NULL,
  `apellidos` VARCHAR(100) NOT NULL,
  `fecha_nacimiento` DATE NOT NULL,
  PRIMARY KEY (`id_paciente`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`personal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`personal` (
  `id_personal` INT NOT NULL AUTO_INCREMENT,
  `nombres` VARCHAR(100) NOT NULL,
  `apellidos` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_personal`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`medicamentos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`medicamento` (
  `id_medicamento` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` VARCHAR(200) NOT NULL,
  `stock_actual` INT NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_medicamento`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`tipo_sangre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`tipo_sangre` (
  `id_tipo_sangre` INT NOT NULL AUTO_INCREMENT,
  `tipo_sangre` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`id_tipo_sangre`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`alegrias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`alergia` (
  `id_alergia` INT NOT NULL AUTO_INCREMENT,
  `nombre_alergia` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_alergia`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`rol` (
  `id_rol` INT NOT NULL AUTO_INCREMENT,
  `nombre_rol` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_rol`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`alergia_paciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`alergia_paciente` (
  `id_alergia_paciente` INT NOT NULL AUTO_INCREMENT,
  `id_paciente` INT NOT NULL,
  `id_alergia` INT NOT NULL,
  PRIMARY KEY (`id_alergia_paciente`),
  INDEX `alergia_paciente_idx` (`id_alergia` ASC) VISIBLE,
  INDEX `paciente_alergia_idx` (`id_paciente` ASC) VISIBLE,
  CONSTRAINT `alergia_paciente`
    FOREIGN KEY (`id_alergia`)
    REFERENCES `clinica_medica`.`alergia` (`id_alergia`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `paciente_alergia`
    FOREIGN KEY (`id_paciente`)
    REFERENCES `clinica_medica`.`paciente` (`id_paciente`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`consulta`
-- CAMBIO: motivo_visita ahora es texto libre, no catalogo
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`consulta` (
  `id_consulta` INT NOT NULL AUTO_INCREMENT,
  `id_paciente` INT NOT NULL,
  `id_medico` INT NOT NULL,
  `id_recepcion` INT NOT NULL,
  `fecha_hora` DATETIME NOT NULL,
  `motivo_visita` VARCHAR(1000) NOT NULL,
  PRIMARY KEY (`id_consulta`),
  INDEX `paciente_consulta_idx` (`id_paciente` ASC) VISIBLE,
  INDEX `medico_consulta_idx` (`id_medico` ASC) VISIBLE,
  INDEX `recepcion_consulta_idx` (`id_recepcion` ASC) VISIBLE,
  CONSTRAINT `paciente_consulta`
    FOREIGN KEY (`id_paciente`)
    REFERENCES `clinica_medica`.`paciente` (`id_paciente`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `medico_consulta`
    FOREIGN KEY (`id_medico`)
    REFERENCES `clinica_medica`.`personal` (`id_personal`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `recepcion_consulta`
    FOREIGN KEY (`id_recepcion`)
    REFERENCES `clinica_medica`.`personal` (`id_personal`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`receta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`receta` (
  `id_receta` INT NOT NULL AUTO_INCREMENT,
  `id_consulta` INT NOT NULL,
  PRIMARY KEY (`id_receta`),
  INDEX `consulta_receta_idx` (`id_consulta` ASC) VISIBLE,
  CONSTRAINT `consulta_receta`
    FOREIGN KEY (`id_consulta`)
    REFERENCES `clinica_medica`.`consulta` (`id_consulta`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`detalles_receta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`detalles_receta` (
  `id_detalles_receta` INT NOT NULL AUTO_INCREMENT,
  `id_receta` INT NOT NULL,
  `id_medicamento` INT NOT NULL,
  `dosis` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_detalles_receta`),
  INDEX `receta_detalles_idx` (`id_receta` ASC) VISIBLE,
  INDEX `medicamento_detalles_idx` (`id_medicamento` ASC) VISIBLE,
  CONSTRAINT `receta_detalles`
    FOREIGN KEY (`id_receta`)
    REFERENCES `clinica_medica`.`receta` (`id_receta`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `medicamento_detalles`
    FOREIGN KEY (`id_medicamento`)
    REFERENCES `clinica_medica`.`medicamento` (`id_medicamento`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`detalles_consulta`
-- CAMBIO: diagnostico y nota_medica son texto libre (NULL
-- hasta que el medico atienda). Solo queda FK a consulta.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`detalles_consulta` (
  `id_detalles_consulta` INT NOT NULL AUTO_INCREMENT,
  `id_consulta` INT NOT NULL,
  `diagnostico` VARCHAR(1000) NULL,
  `nota_medica` VARCHAR(1000) NULL,
  `fecha_atencion` DATETIME NULL,
  PRIMARY KEY (`id_detalles_consulta`),
  INDEX `consulta_detalles_idx` (`id_consulta` ASC) VISIBLE,
  CONSTRAINT `consulta_detalles`
    FOREIGN KEY (`id_consulta`)
    REFERENCES `clinica_medica`.`consulta` (`id_consulta`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`paciente_sangre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`paciente_sangre` (
  `id_paciente_sangre` INT NOT NULL AUTO_INCREMENT,
  `id_paciente` INT NOT NULL,
  `id_tipo_sangre` INT NOT NULL,
  PRIMARY KEY (`id_paciente_sangre`),
  INDEX `paciente_tipo_sangre_idx` (`id_paciente` ASC) VISIBLE,
  INDEX `tipo_sangre_paciente_idx` (`id_tipo_sangre` ASC) VISIBLE,
  CONSTRAINT `paciente_tipo_sangre`
    FOREIGN KEY (`id_paciente`)
    REFERENCES `clinica_medica`.`paciente` (`id_paciente`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tipo_sangre_paciente`
    FOREIGN KEY (`id_tipo_sangre`)
    REFERENCES `clinica_medica`.`tipo_sangre` (`id_tipo_sangre`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`numero_colegiado`
-- Se mantiene aparte: solo los medicos tienen colegiacion
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`numero_colegiado` (
  `id_numero_colegiado` INT NOT NULL AUTO_INCREMENT,
  `numero_colegiado` INT NOT NULL,
  PRIMARY KEY (`id_numero_colegiado`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`personal_numero_colegiado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`personal_numero_colegiado` (
  `id_personal_numero_colegiado` INT NOT NULL AUTO_INCREMENT,
  `id_personal` INT NOT NULL,
  `id_numero_colegiado` INT NOT NULL,
  PRIMARY KEY (`id_personal_numero_colegiado`),
  INDEX `personal_colegiado_idx` (`id_personal` ASC) VISIBLE,
  INDEX `colegiado_personal_idx` (`id_numero_colegiado` ASC) VISIBLE,
  CONSTRAINT `personal_colegiado`
    FOREIGN KEY (`id_personal`)
    REFERENCES `clinica_medica`.`personal` (`id_personal`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `colegiado_personal`
    FOREIGN KEY (`id_numero_colegiado`)
    REFERENCES `clinica_medica`.`numero_colegiado` (`id_numero_colegiado`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`personal_rol`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`personal_rol` (
  `id_personal_rol` INT NOT NULL AUTO_INCREMENT,
  `id_personal` INT NOT NULL,
  `id_rol` INT NOT NULL,
  PRIMARY KEY (`id_personal_rol`),
  INDEX `rol_personal_idx` (`id_rol` ASC) VISIBLE,
  INDEX `personal_rol_idx` (`id_personal` ASC) VISIBLE,
  CONSTRAINT `rol_personal`
    FOREIGN KEY (`id_rol`)
    REFERENCES `clinica_medica`.`rol` (`id_rol`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `personal_rol`
    FOREIGN KEY (`id_personal`)
    REFERENCES `clinica_medica`.`personal` (`id_personal`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`datos_factura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`datos_factura` (
  `id_datos_factura` INT NOT NULL AUTO_INCREMENT,
  `nit` VARCHAR(45) NOT NULL,
  `direccion` VARCHAR(100) NOT NULL,
  `detalles` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_datos_factura`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`ventas`
-- CAMBIO: se agrega la FK faltante id_personal -> personal
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`venta` (
  `id_venta` INT NOT NULL AUTO_INCREMENT,
  `id_datos_factura` INT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `fecha_hora` DATETIME NOT NULL,
  `id_personal` INT NOT NULL,
  `total` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX `datos_factura_idx` (`id_datos_factura` ASC) VISIBLE,
  INDEX `personal_ventas_idx` (`id_personal` ASC) VISIBLE,
  CONSTRAINT `datos_factura`
    FOREIGN KEY (`id_datos_factura`)
    REFERENCES `clinica_medica`.`datos_factura` (`id_datos_factura`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `personal_ventas`
    FOREIGN KEY (`id_personal`)
    REFERENCES `clinica_medica`.`personal` (`id_personal`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `clinica_medica`.`detalles_ventas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica_medica`.`detalles_venta` (
  `id_detalles_venta` INT NOT NULL AUTO_INCREMENT,
  `id_venta` INT NOT NULL,
  `id_medicamento` INT NOT NULL,
  `cantidad` INT NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_detalles_venta`),
  INDEX `factura_detalles_idx` (`id_venta` ASC) VISIBLE,
  INDEX `medicamentos_detalles_idx` (`id_medicamento` ASC) VISIBLE,
  CONSTRAINT `factura_detalles`
    FOREIGN KEY (`id_venta`)
    REFERENCES `clinica_medica`.`venta` (`id_venta`)
    ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `medicamentos_detalles`
    FOREIGN KEY (`id_medicamento`)
    REFERENCES `clinica_medica`.`medicamento` (`id_medicamento`)
    ON DELETE RESTRICT ON UPDATE RESTRICT)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `clinica_medica`.`usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `id_personal` INT NOT NULL,
  `nombre_usuario` VARCHAR(50) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NULL,
  `activo` TINYINT(1) DEFAULT 1,
  PRIMARY KEY (`id_usuario`),
  CONSTRAINT `usuario_personal`
    FOREIGN KEY (`id_personal`)
    REFERENCES `clinica_medica`.`personal` (`id_personal`)
    ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB;

ALTER TABLE `clinica_medica`.`usuario`
MODIFY COLUMN `activo` TINYINT DEFAULT 1;
-- *********************************************** --
ALTER TABLE clinica_medica.detalles_receta 
MODIFY COLUMN id_medicamento INT NULL;

ALTER TABLE clinica_medica.detalles_receta 
ADD COLUMN nombre_medicamento VARCHAR(150) NULL AFTER id_medicamento;
-- *********************************************************************** --
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



