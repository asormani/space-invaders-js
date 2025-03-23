
// Configurações do jogo
const GAME_WIDTH = 600;
const GAME_HEIGHT = 600;
const PLAYER_SPEED = 5;
const ALIEN_ROW_COUNT = 5;
const ALIEN_COLUMN_COUNT = 8;
const GAME_STATE = {
    MENU: 'menu',
    PLAYING: 'playing',
    GAME_OVER: 'gameOver'
};

// Imagens do jogo
const IMAGES = {
    player: null,
    redAlien: null,
    redAlien2: null,
    greenAlien: null,
    greenAlien2: null,
    yellowAlien: null,
    yellowAlien2: null,
    extraShip: null,
    explosion: null
};

// Sons do jogo
const SOUNDS = {
    playerShoot: null,
    alienShoot: null,
    explosion: null,
    playerExplosion: null,
    extraShip: null,
    extraExplosion: null,
    gameMusic: null
};

let game;

// Classe principal do jogo
class Game {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = GAME_WIDTH;
        this.canvas.height = GAME_HEIGHT;

        this.state = GAME_STATE.MENU;
        this.score = 0;
        this.lives = 3;
        this.level = 1;
        this.highScore = localStorage.getItem('spaceInvadersHighScore') || 0;
        document.getElementById('high-score').textContent = this.highScore;

        this.player = null;
        this.aliens = [];
        this.alienSpeed = 1;
        this.playerLasers = [];
        this.alienLasers = [];
        this.barriers = [];
        this.extraShip = null;
        this.extraShipTimer = 0;

        this.keys = {
            left: false,
            right: false,
            space: false,
            enter: false
        };

        this.setup();
        this.loadAssets();
        this.bindEvents();

        // Iniciar o loop do jogo
        this.lastTime = 0;
        requestAnimationFrame(this.gameLoop.bind(this));

        game = this;
    }

    setup() {
        // Configurar elementos iniciais do jogo
        this.resetGame();
    }

    resetGame() {
        this.score = 0;
        this.lives = 3;
        this.level = 1;

        // Criar o jogador
        this.player = new Player();

        // Criar os aliens
        this.createAliens();

        // Criar as barreiras
        this.createBarriers();

        // Limpar os lasers
        this.playerLasers = [];
        this.alienLasers = [];

        // Resetar o extra ship
        this.extraShip = null;
        this.extraShipTimer = Math.floor(Math.random() * 500) + 500;
    }

    createAliens() {
        this.aliens = [];

        const startX = 70;
        const startY = 100;
        const xSpacing = 60;
        const ySpacing = 48;

        for (let row = 0; row < ALIEN_ROW_COUNT; row++) {
            for (let col = 0; col < ALIEN_COLUMN_COUNT; col++) {
                let type;
                if (row === 0) {
                    type = 'yellow';
                } else if (row <= 2) {
                    type = 'green';
                } else {
                    type = 'red';
                }

                const x = startX + col * xSpacing;
                const y = startY + row * ySpacing;

                const alien = new Alien(type, x, y);
                this.aliens.push(alien);
            }
        }
    }

    createBarriers() {
        this.barriers = [];

        const barrierCount = 4;
        const spacing = GAME_WIDTH / barrierCount;

        for (let i = 0; i < barrierCount; i++) {
            const x = spacing * i + spacing / 2 - 50;
            const barrier = new Barrier(x, 480);
            this.barriers.push(barrier);
        }
    }

    loadAssets() {
        // Carregar imagens
        IMAGES.player = new Image();
        IMAGES.player.src = 'graphics/player.png';

        IMAGES.redAlien = new Image();
        IMAGES.redAlien.src = 'graphics/red.png';
        IMAGES.redAlien2 = new Image();
        IMAGES.redAlien2.src = 'graphics/red2.png';

        IMAGES.greenAlien = new Image();
        IMAGES.greenAlien.src = 'graphics/green.png';
        IMAGES.greenAlien2 = new Image();
        IMAGES.greenAlien2.src = 'graphics/green2.png';

        IMAGES.yellowAlien = new Image();
        IMAGES.yellowAlien.src = 'graphics/yellow.png';
        IMAGES.yellowAlien2 = new Image();
        IMAGES.yellowAlien2.src = 'graphics/yellow2.png';

        IMAGES.extraShip = new Image();
        IMAGES.extraShip.src = 'graphics/extra.png';

        // Carregar sons
        SOUNDS.playerShoot = new Audio();
        SOUNDS.playerShoot.src = 'sons/laser.wav';

        SOUNDS.alienShoot = new Audio();
        SOUNDS.alienShoot.src = 'sons/laser.wav';
        SOUNDS.alienShoot.volume = 0.3;

        SOUNDS.explosion = new Audio();
        SOUNDS.explosion.src = 'sons/explosion.wav';
        SOUNDS.explosion.volume = 0.3;

        SOUNDS.playerExplosion = new Audio();
        SOUNDS.playerExplosion.src = 'sons/shipexplosion.wav';
        SOUNDS.playerExplosion.volume = 0.3;

        SOUNDS.extraShip = new Audio();
        SOUNDS.extraShip.src = 'sons/mysteryentered.wav';
        SOUNDS.extraShip.volume = 0.3;

        SOUNDS.extraExplosion = new Audio();
        SOUNDS.extraExplosion.src = 'sons/mysterykilled.wav';
        SOUNDS.extraExplosion.volume = 0.4;

        SOUNDS.gameMusic = new Audio();
        SOUNDS.gameMusic.src = 'sons/music.wav';
        SOUNDS.gameMusic.loop = true;
        SOUNDS.gameMusic.volume = 0.2;
    }

    bindEvents() {
        // Adicionar eventos de teclado
        window.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowLeft':
                case 'j':
                    this.keys.left = true;
                    break;
                case 'ArrowRight':
                case 'k':
                    this.keys.right = true;
                    break;
                case ' ':
                case 'w':
                    this.keys.space = true;
                    if (this.state === GAME_STATE.PLAYING) {
                        this.playerShoot();
                    }
                    break;
                case 'Enter':
                    this.keys.enter = true;
                    if (this.state === GAME_STATE.MENU) {
                        this.startGame();
                    } else if (this.state === GAME_STATE.GAME_OVER) {
                        this.state = GAME_STATE.MENU;
                        document.getElementById('game-over-screen').style.display = 'none';
                        document.getElementById('start-screen').style.display = 'flex';
                    }
                    break;
                case 'Escape':
                    if (this.state === GAME_STATE.PLAYING) {
                        this.state = GAME_STATE.MENU;
                        document.getElementById('start-screen').style.display = 'flex';
                        SOUNDS.gameMusic.pause();
                    }
                    break;
            }
        });

        window.addEventListener('keyup', (e) => {
            switch (e.key) {
                case 'ArrowLeft':
                case 'j':
                    this.keys.left = false;
                    break;
                case 'ArrowRight':
                case 'k':
                    this.keys.right = false;
                    break;
                case ' ':
                case 'w':
                    this.keys.space = false;
                    break;
                case 'Enter':
                    this.keys.enter = false;
                    break;
            }
        });

        // Dentro da classe Game, no método bindEvents():
        const orientationHandler = (e) => {
            if (game.state !== GAME_STATE.PLAYING) return;
            const gamma = e.gamma; // Inclinação lateral
            if (gamma > 10) { // Inclinação para a direita
                game.player.moveRight();
            } else if (gamma < -10) { // Inclinação para a esquerda
                game.player.moveLeft();
            }
        };

        if (typeof DeviceOrientationEvent.requestPermission === 'function') {
            DeviceOrientationEvent.requestPermission()
                .then(permissionState => {
                    if (permissionState === 'granted') {
                        window.addEventListener('deviceorientation', orientationHandler, { passive: false});
                    } else {
                        console.log('Permissão de orientação do dispositivo negada.');
                    }
                })
                .catch(console.error);
        } else {
            window.addEventListener('deviceorientation', orientationHandler, { passive: false});
        }

        // Adicionar botões de seta para dispositivos móveis
        const createArrowButtons = () => {
            const leftBtn = document.createElement('div');
            leftBtn.id = 'left-btn';
            leftBtn.className = 'arrow-btn';
            document.body.appendChild(leftBtn);

            const rightBtn = document.createElement('div');
            rightBtn.id = 'right-btn';
            rightBtn.className = 'arrow-btn';
            document.body.appendChild(rightBtn);

            leftBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.keys.left = true;
            });

            leftBtn.addEventListener('touchend', (e) => {
                e.preventDefault();
                this.keys.left = false;
            });

            rightBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.keys.right = true;
            });

            rightBtn.addEventListener('touchend', (e) => {
                e.preventDefault();
                this.keys.right = false;
            });
        };

        // Adicionar toque para iniciar o jogo
        const touchStartHandler = (e) => {
            e.preventDefault();
            if (e.target.id === 'left-btn' || e.target.id === 'right-btn' || e.target.id === 'shoot-btn') return;
            if (this.state === GAME_STATE.MENU || this.state === GAME_STATE.GAME_OVER) {
                this.keys.enter = true;
                if (this.state === GAME_STATE.MENU) {
                    this.startGame();
                } else if (this.state === GAME_STATE.GAME_OVER) {
                    this.state = GAME_STATE.MENU;
                    document.getElementById('game-over-screen').style.display = 'none';
                    document.getElementById('start-screen').style.display = 'flex';
                }
            }
        };

        
        // Adicionar botão de tiro para dispositivos móveis
        const createShootButton = () => {
            const shootBtn = document.createElement('div');
            shootBtn.id = 'shoot-btn';
            shootBtn.className = 'mobile-control';
            document.body.appendChild(shootBtn);

            shootBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                e.stopPropagation(); // Impede que outros eventos de toque sejam acionados
                if (this.state === GAME_STATE.PLAYING) {
                    this.playerShoot();
                }
            });
        };

        // Verificar se é um dispositivo móvel
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        if (isMobile) {
            createArrowButtons();
            window.addEventListener('touchstart', touchStartHandler, { passive: false });
            createShootButton();
        }
    }

    startGame() {
        this.state = GAME_STATE.PLAYING;
        document.getElementById('start-screen').style.display = 'none';
        this.resetGame();
        SOUNDS.gameMusic.currentTime = 0;
        SOUNDS.gameMusic.play();
    }

    gameOver() {
        this.state = GAME_STATE.GAME_OVER;
        SOUNDS.gameMusic.pause();
        if (window.DeviceOrientationEvent) {
            window.removeEventListener('deviceorientation', orientationHandler);

        // Verificar recorde
        if (this.score > this.highScore) {
            this.highScore = this.score;
            localStorage.setItem('spaceInvadersHighScore', this.highScore);
            document.getElementById('high-score').textContent = this.highScore;
        }

        // Mostrar tela de game over
        document.getElementById('final-score').textContent = this.score;
        document.getElementById('final-level').textContent = this.level;
        document.getElementById('game-over-screen').style.display = 'flex';
    }

    update(deltaTime) {
        if (this.state !== GAME_STATE.PLAYING) return;

        // Atualizar jogador
        if (this.keys.left) {
            this.player.moveLeft();
        }
        if (this.keys.right) {
            this.player.moveRight();
        }

        // Atualizar posição do jogador
        this.player.update();

        // Atualizar lasers do jogador
        for (let i = this.playerLasers.length - 1; i >= 0; i--) {
            this.playerLasers[i].update();

            // Remover laser se saiu da tela
            if (this.playerLasers[i].isOffScreen()) {
                this.playerLasers.splice(i, 1);
                continue;
            }

            // Verificar colisão com aliens
            for (let j = this.aliens.length - 1; j >= 0; j--) {
                if (this.playerLasers[i] && this.checkCollision(this.playerLasers[i], this.aliens[j])) {
                    this.score += this.aliens[j].value;
                    this.aliens.splice(j, 1);
                    this.playerLasers.splice(i, 1);
                    SOUNDS.explosion.currentTime = 0;
                    SOUNDS.explosion.play();
                    break;
                }
            }

            // Verificar colisão com nave extra
            if (this.playerLasers[i] && this.extraShip && this.checkCollision(this.playerLasers[i], this.extraShip)) {
                this.score += 500;
                SOUNDS.extraExplosion.currentTime = 0;
                SOUNDS.extraExplosion.play();
                this.extraShip = null;
                this.playerLasers.splice(i, 1);
            }

            // Verificar colisão com barreiras
            if (this.playerLasers[i]) {
                for (const barrier of this.barriers) {
                    if (barrier.checkCollision(this.playerLasers[i])) {
                        this.playerLasers.splice(i, 1);
                        break;
                    }
                }
            }
        }

        // Atualizar lasers dos aliens
        for (let i = this.alienLasers.length - 1; i >= 0; i--) {
            this.alienLasers[i].update();

            // Remover laser se saiu da tela
            if (this.alienLasers[i].isOffScreen()) {
                this.alienLasers.splice(i, 1);
                continue;
            }

            // Verificar colisão com o jogador
            if (this.checkCollision(this.alienLasers[i], this.player)) {
                this.lives--;
                this.alienLasers.splice(i, 1);
                SOUNDS.playerExplosion.currentTime = 0;
                SOUNDS.playerExplosion.play();

                if (this.lives <= 0) {
                    this.gameOver();
                    return;
                }

                continue;
            }

            // Verificar colisão com barreiras
            for (const barrier of this.barriers) {
                if (barrier.checkCollision(this.alienLasers[i])) {
                    this.alienLasers.splice(i, 1);
                    break;
                }
            }
        }

        // Atualizar aliens
        let moveDown = false;
        let direction = 1;

        // Verificar se algum alien atingiu as bordas
        for (const alien of this.aliens) {
            if (alien.x + alien.width >= GAME_WIDTH || alien.x <= 0) {
                moveDown = true;
                direction = alien.x <= 0 ? 1 : -1;
                break;
            }
        }

        // Mover aliens
        for (const alien of this.aliens) {
            if (moveDown) {
                alien.y += 5;
                alien.direction = direction;
            }
            alien.update();

            // Verificar se algum alien chegou na parte inferior (invasão)
            if (alien.y + alien.height >= this.player.y) {
                this.lives = 0;
                this.gameOver();
                return;
            }
        }

        // Alien atirar aleatoriamente
        if (Math.random() < 0.01 + (this.level * 0.003) && this.aliens.length > 0) {
            const randomAlien = this.aliens[Math.floor(Math.random() * this.aliens.length)];
            this.alienShoot(randomAlien);
        }

        // Atualizar nave extra
        this.extraShipTimer--;
        if (this.extraShipTimer <= 0 && !this.extraShip) {
            this.createExtraShip();
        }

        if (this.extraShip) {
            this.extraShip.update();

            // Remover nave extra se saiu da tela
            if ((this.extraShip.direction > 0 && this.extraShip.x > GAME_WIDTH + 50) || 
                (this.extraShip.direction < 0 && this.extraShip.x < -50)) {
                this.extraShip = null;
                this.extraShipTimer = Math.floor(Math.random() * 500) + 500;
            }
        }

        // Verificar se todos os aliens foram eliminados
        if (this.aliens.length === 0) {
            this.advanceLevel();
        }
    }

    draw() {
        // Limpar o canvas
        this.ctx.fillStyle = '#1e1e1e';
        this.ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

        if (this.state === GAME_STATE.PLAYING) {
            // Desenhar jogador
            this.player.draw(this.ctx);

            // Desenhar aliens
            for (const alien of this.aliens) {
                alien.draw(this.ctx);
            }

            // Desenhar lasers do jogador
            for (const laser of this.playerLasers) {
                laser.draw(this.ctx);
            }

            // Desenhar lasers dos aliens
            for (const laser of this.alienLasers) {
                laser.draw(this.ctx);
            }

            // Desenhar barreiras
            for (const barrier of this.barriers) {
                barrier.draw(this.ctx);
            }

            // Desenhar nave extra
            if (this.extraShip) {
                this.extraShip.draw(this.ctx);
            }

            // Desenhar informações
            this.drawInfo();
        }

        // Aplicar efeito CRT
        this.applyCRTEffect();
    }

    drawInfo() {
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '16px monospace';
        this.ctx.fillText(`Score: ${this.score}`, 10, 25);
        this.ctx.fillText(`Level: ${this.level}`, GAME_WIDTH / 2 - 40, 25);

        // Desenhar vidas
        this.ctx.fillText(`Lives:`, GAME_WIDTH - 100, 25);
        for (let i = 0; i < this.lives; i++) {
            this.ctx.fillStyle = '#0f0';
            this.ctx.fillRect(GAME_WIDTH - 60 + (i * 15), 15, 10, 5);
        }
    }

    applyCRTEffect() {
        // Simular efeito CRT com linhas horizontais
        this.ctx.globalAlpha = 0.1;
        this.ctx.fillStyle = '#000';
        for (let i = 0; i < GAME_HEIGHT; i += 4) {
            this.ctx.fillRect(0, i, GAME_WIDTH, 2);
        }
        this.ctx.globalAlpha = 1.0;
    }

    playerShoot() {
        if (this.playerLasers.length < 3) { // Limitar a 3 lasers simultâneos
            const laser = new Laser(
                this.player.x + this.player.width / 2,
                this.player.y,
                -8 // Velocidade negativa (para cima)
            );
            this.playerLasers.push(laser);
            SOUNDS.playerShoot.currentTime = 0;
            SOUNDS.playerShoot.play();
        }
    }

    alienShoot(alien) {
        const laser = new Laser(
            alien.x + alien.width / 2,
            alien.y + alien.height,
            4 // Velocidade positiva (para baixo)
        );
        this.alienLasers.push(laser);
        SOUNDS.alienShoot.currentTime = 0;
        SOUNDS.alienShoot.play();
    }

    createExtraShip() {
        const direction = Math.random() < 0.5 ? 1 : -1;
        const x = direction < 0 ? GAME_WIDTH + 50 : -50;
        this.extraShip = new ExtraShip(x, 50, direction);
        SOUNDS.extraShip.currentTime = 0;
        SOUNDS.extraShip.play();
    }

    advanceLevel() {
        this.level++;
        this.alienSpeed += 0.2;
        this.createAliens();

        // Recriar barreiras a cada 3 níveis
        if (this.level % 3 === 1) {
            this.createBarriers();
        }
    }

    checkCollision(obj1, obj2) {
        return obj1.x < obj2.x + obj2.width &&
               obj1.x + obj1.width > obj2.x &&
               obj1.y < obj2.y + obj2.height &&
               obj1.y + obj1.height > obj2.y;
    }

    gameLoop(timestamp) {
        // Calcular delta time
        const deltaTime = timestamp - this.lastTime;
        this.lastTime = timestamp;

        // Atualizar e desenhar o jogo
        this.update(deltaTime);
        this.draw();

        // Continuar o loop de jogo
        requestAnimationFrame(this.gameLoop.bind(this));
    }
}

// Classe do jogador
class Player {
    constructor() {
        this.width = 50;
        this.height = 36;
        this.x = GAME_WIDTH / 2 - this.width / 2;
        this.y = GAME_HEIGHT - 50;
        this.speed = PLAYER_SPEED;
    }

    update() {
        // Restringir movimento às bordas da tela
        if (this.x < 0) {
            this.x = 0;
        }
        if (this.x + this.width > GAME_WIDTH) {
            this.x = GAME_WIDTH - this.width;
        }
    }

    moveLeft() {
        this.x -= this.speed;
    }

    moveRight() {
        this.x += this.speed;
    }

    draw(ctx) {
        if (IMAGES.player && IMAGES.player.complete) {
            ctx.drawImage(IMAGES.player, this.x, this.y, this.width, this.height);
        } else {
            // Fallback se a imagem não estiver carregada
            ctx.fillStyle = '#0f0';
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }
}

// Classe de alien
class Alien {
    constructor(type, x, y) {
        this.type = type;
        this.width = 50;
        this.height = 36;
        this.x = x;
        this.y = y;
        this.direction = 1;
        this.animationFrame = 0;
        this.animationTimer = 0;
        this.animationSpeed = 30; // Velocidade da animação

        // Valor de pontos baseado no tipo
        switch (type) {
            case 'red':
                this.value = 100;
                this.color = '#ff0000';
                break;
            case 'green':
                this.value = 200;
                this.color = '#00ff00';
                break;
            case 'yellow':
                this.value = 300;
                this.color = '#ffff00';
                break;
        }
    }

    update() {
        this.x += this.direction * game.alienSpeed;

        // Atualiza a animação
        this.animationTimer++;
        if (this.animationTimer >= this.animationSpeed) {
            this.animationFrame = this.animationFrame === 0 ? 1 : 0;
            this.animationTimer = 0;
        }
    }

    draw(ctx) {
        let image = null;

        // Seleciona a imagem base no tipo e no frame atual da animação
        switch (this.type) {
            case 'red':
                image = this.animationFrame === 0 ? IMAGES.redAlien : IMAGES.redAlien2;
                break;
            case 'green':
                image = this.animationFrame === 0 ? IMAGES.greenAlien : IMAGES.greenAlien2;
                break;
            case 'yellow':
                image = this.animationFrame === 0 ? IMAGES.yellowAlien : IMAGES.yellowAlien2;
                break;
        }

        if (image && image.complete) {
            ctx.drawImage(image, this.x, this.y, this.width, this.height);
        } else {
            // Fallback se a imagem não estiver carregada
            ctx.fillStyle = this.color;
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }
}

// Classe de nave extra
class ExtraShip {
    constructor(x, y, direction) {
        this.width = 50;
        this.height = 24;
        this.x = x;
        this.y = y;
        this.direction = direction;
        this.speed = 2 * direction;
    }

    update() {
        this.x += this.speed;
    }

    draw(ctx) {
        if (IMAGES.extraShip && IMAGES.extraShip.complete) {
            ctx.drawImage(IMAGES.extraShip, this.x, this.y, this.width, this.height);
        } else {
            // Fallback se a imagem não estiver carregada
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }
}

// Classe de laser
class Laser {
    constructor(x, y, speed) {
        this.width = 4;
        this.height = 15;
        this.x = x - this.width / 2;
        this.y = y;
        this.speed = speed;
    }

    update() {
        this.y += this.speed;
    }

    isOffScreen() {
        return this.y < -this.height || this.y > GAME_HEIGHT;
    }

    draw(ctx) {
        ctx.fillStyle = '#fff';
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
}

// Classe de barreira
class Barrier {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.blocks = [];
        this.createBlocks();
    }

    createBlocks() {
        const shape = [
            '  xxxxx ',
            ' xxxxxxx',
            'xxxxxxxxx',
            'xxxxxxxxx',
            'xxxxxxxxx',
            'xxx   xxx',
            'xx     xx'
        ];

        const blockSize = 6;

        for (let row = 0; row < shape.length; row++) {
            for (let col = 0; col < shape[row].length; col++) {
                if (shape[row][col] === 'x') {
                    const block = {
                        x: this.x + col * blockSize,
                        y: this.y + row * blockSize,
                        width: blockSize,
                        height: blockSize
                    };
                    this.blocks.push(block);
                }
            }
        }
    }

    checkCollision(obj) {
        for (let i = this.blocks.length - 1; i >= 0; i--) {
            const block = this.blocks[i];
            if (obj.x < block.x + block.width &&
                obj.x + obj.width > block.x &&
                obj.y < block.y + block.height &&
                obj.y + obj.height > block.y) {

                this.blocks.splice(i, 1);
                return true;
            }
        }
        return false;
    }

    draw(ctx) {
        ctx.fillStyle = '#f14f4f';
        for (const block of this.blocks) {
            ctx.fillRect(block.x, block.y, block.width, block.height);
        }
    }
}

// Iniciar o jogo quando o documento for carregado
document.addEventListener('DOMContentLoaded', () => {
    new Game();
});
