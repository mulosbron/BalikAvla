import pygame
import random
import skorTablosu

# Pygame Hazırlık
pygame.init()

# Pencere Ayarları
GENISLIK, YUKSEKLIK = 750, 750
pencere = pygame.display.set_mode((GENISLIK, YUKSEKLIK))

# FPS Ayarları
FPS = 60
saat = pygame.time.Clock()


# Sınıflar
class Balik(pygame.sprite.Sprite):
	def __init__(self, x, y, resim, tip):
		super().__init__()
		self.image = resim
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.tip = tip
		self.hiz = 2

		# Sınırları Ayarlama
		self.yonx = random.choice([-1, 1])
		self.yony = random.choice([-1, 1])

	def update(self):
		# yonx ile çarpıyoruz ve balığımız x ekseninde gideceği rastgele yönü seçiyor.
		self.rect.x += self.hiz * self.yonx
		self.rect.y += self.hiz * self.yony
		if self.rect.left <= 0 or self.rect.right >= GENISLIK:
			self.yonx *= -1
		if self.rect.top <= 100 or self.rect.bottom >= YUKSEKLIK - 50:
			self.yony *= -1


class BuyukBalik(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("buyuk_balik.png")
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.can = 5
		self.hiz = 7

	def update(self):
		self.hareket()

	def hareket(self):
		tus = pygame.key.get_pressed()
		global durum
		if tus[pygame.K_ESCAPE]:
			durum = False
		if tus[pygame.K_LEFT] and tus[pygame.K_UP] and self.rect.top > 100 and self.rect.left > 0:
			self.rect.x -= self.hiz - 2
			self.rect.y -= self.hiz - 2
		elif tus[pygame.K_LEFT] and tus[pygame.K_DOWN] and self.rect.bottom < YUKSEKLIK - 50 and self.rect.left > 0:
			self.rect.x -= self.hiz - 2
			self.rect.y += self.hiz - 2
		elif tus[pygame.K_RIGHT] and tus[pygame.K_UP] and self.rect.right < GENISLIK and self.rect.top > 100:
			self.rect.x += self.hiz - 2
			self.rect.y -= self.hiz - 2
		elif tus[pygame.K_RIGHT] and tus[
			pygame.K_DOWN] and self.rect.right < GENISLIK and self.rect.bottom < YUKSEKLIK - 50:
			self.rect.x += self.hiz - 2
			self.rect.y += self.hiz - 2
		elif tus[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= self.hiz
		elif tus[pygame.K_RIGHT] and self.rect.right < GENISLIK:
			self.rect.x += self.hiz
		elif tus[pygame.K_UP] and self.rect.top > 100:
			self.rect.y -= self.hiz
		elif tus[pygame.K_DOWN] and self.rect.bottom < YUKSEKLIK - 50:
			self.rect.y += self.hiz


class Oyun:
	def __init__(self, _balikci, _balik_grup):
		# Nesneler
		self.balikci = _balikci
		self.balik_grup = _balik_grup
		# Oyun değişkenleri
		self.sure = 0
		self.fps_degeri_sayma = 0
		self.bolum_no = 0
		self.skor = 0
		# Balıklar (Yakalamamız gereken balık için yapılan ayarlar)
		self.balikListe = list()
		for j in range(1, 5):
			balikOyun = pygame.image.load(f"balik{j}.png")
			self.balikListe.append(balikOyun)
		self.balik_liste_index_no = random.randint(0, 3)
		self.hedef_balik_goruntu = self.balikListe[self.balik_liste_index_no]
		self.hedef_balik_konum = self.hedef_balik_goruntu.get_rect()
		self.hedef_balik_konum.top = 40
		self.hedef_balik_konum.centerx = GENISLIK // 2
		# Font
		self.oyun_font = pygame.font.Font("oyun_font.ttf", 40)
		# Oyun Müzikleri ve Ses Efektleri
		self.balik_tutma = pygame.mixer.Sound("yeme_efekt.wav")
		self.olme_sesi = pygame.mixer.Sound("olu.wav")
		pygame.mixer.music.load("sarki.wav")
		# Oyun bitene kadar müziği çaldırmak için -1 değerini girdik.
		pygame.mixer.music.play(-1)
		# Arka Plan
		self.oyun_arka_plan = pygame.image.load("arka_plan.jpg")
		self.oyun_bitti = pygame.image.load("oyun_sonu.jpg")

	def update(self):
		self.fps_degeri_sayma += 1
		if self.fps_degeri_sayma == FPS:
			self.sure += 1
			self.fps_degeri_sayma = 0
		self.temas()

	def cizdir(self):
		# Süre metni
		metin_sure = self.oyun_font.render("Süre: " + str(self.sure), True, (255, 255, 255), (0, 0, 170))
		metin_sure_konum = metin_sure.get_rect()
		metin_sure_konum.top = 30
		metin_sure_konum.left = 30
		# Can metni
		metin_can = self.oyun_font.render("Can: " + str(self.balikci.can), True, (255, 255, 255), (0, 0, 170))
		metin_can_konum = metin_can.get_rect()
		metin_can_konum.top = 30
		metin_can_konum.left = GENISLIK - 130
		# Skor metni
		metin_skor = self.oyun_font.render("Skor: " + str(self.skor), True, (255, 255, 255), (0, 0, 170))
		metin_skor_konum = metin_skor.get_rect()
		metin_skor_konum.top = 30
		metin_skor_konum.left = GENISLIK // 2 - 185
		# Bölüm metni
		metin_bolum = self.oyun_font.render("Bölüm: " + str(self.bolum_no), True, (255, 255, 255), (0, 0, 170))
		metin_bolum_konum = metin_bolum.get_rect()
		metin_bolum_konum.top = 30
		metin_bolum_konum.left = GENISLIK // 2 + 65
		# Arka Plan
		pencere.blit(self.oyun_arka_plan, (0, 0))
		# Süre
		pencere.blit(metin_sure, metin_sure_konum)
		# Can
		pencere.blit(metin_can, metin_can_konum)
		# Skor
		pencere.blit(metin_skor, metin_skor_konum)
		# Bölüm
		pencere.blit(metin_bolum, metin_bolum_konum)
		# Üstte yakalamamız gereken balığı gösteren görüntü
		pencere.blit(self.hedef_balik_goruntu, self.hedef_balik_konum)

		pygame.draw.rect(pencere, (255, 255, 255), (350, 30, 50, 50), 5)
		pygame.draw.rect(pencere, (0, 0, 200), (0, 100, 750, YUKSEKLIK - 150), 5)

	def temas(self):
		temas_var_mi = pygame.sprite.spritecollideany(self.balikci, self.balik_grup)
		if temas_var_mi:
			if temas_var_mi.tip == self.balik_liste_index_no:
				temas_var_mi.remove(self.balik_grup)
				self.balik_tutma.play()
				if self.balik_grup:
					self.hedef_yenile()
				else:
					self.hedefle()
				self.skor += 1
			else:
				self.balikci.can -= 1
				self.olme_sesi.play()
				self.guvenli_alan()
				if self.balikci.can <= 0:
					self.durdur()

	def oyun_bitti_cizdir(self):
		# Arka Plan
		pencere.blit(self.oyun_bitti, (0, 0))
		# Skorlar Metni
		metin_skorlar_tus = self.oyun_font.render("S - Skorları görüntüle", True, (255, 255, 255), (0, 0, 170))
		metin_skorlar_tus_konum = metin_skorlar_tus.get_rect()
		metin_skorlar_tus_konum.top = YUKSEKLIK - 185
		metin_skorlar_tus_konum.left = 120
		# Reset Metni
		metin_reset_tus = self.oyun_font.render("SPACE - Oyuna yeniden basla", True, (255, 255, 255), (0, 0, 170))
		metin_reset_tus_konum = metin_reset_tus.get_rect()
		metin_reset_tus_konum.top = YUKSEKLIK - 125
		metin_reset_tus_konum.left = 120
		# SPACE Tuşu
		pencere.blit(metin_reset_tus, metin_reset_tus_konum)
		# S Tuşu
		pencere.blit(metin_skorlar_tus, metin_skorlar_tus_konum)
		pygame.display.update()

	def durdur(self):
		global durum
		self.oyun_bitti_cizdir()
		self.skor_kayit()
		oyun_durdu = True
		while oyun_durdu:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.reset()
						oyun_durdu = False
					elif event.key == pygame.K_s:
						self.skor_cizdir()
					elif event.key == pygame.K_ESCAPE:
						oyun_durdu = False
						durum = False
				if event.type == pygame.QUIT:
					oyun_durdu = False
					durum = False

	def reset(self):
		self.balikci.can = 3
		self.bolum_no = 0
		self.hedefle()
		self.guvenli_alan()
		self.balikci.rect.center = (GENISLIK // 2, YUKSEKLIK - 40)
		self.sure = 0
		self.skor = 0

	def guvenli_alan(self):
		self.balikci.rect.top = YUKSEKLIK - 40

	def hedef_yenile(self):
		hedef_balik = random.choice(self.balik_grup.sprites())
		self.hedef_balik_goruntu = hedef_balik.image
		self.balik_liste_index_no = hedef_balik.tip

	def hedefle(self):
		self.balikci.rect.center = (GENISLIK // 2, YUKSEKLIK - 25)
		if self.bolum_no % 2 == 0 and self.bolum_no != 0:
			self.balikci.can += 3
		self.bolum_no += 1
		for balik in self.balik_grup:
			self.balik_grup.remove(balik)
		for x in range(self.bolum_no):
			self.balik_grup.add(Balik(random.randint(0, GENISLIK - 32), random.randint(105, YUKSEKLIK - 150),
			                          self.balikListe[0], 0))
			self.balik_grup.add(Balik(random.randint(0, GENISLIK - 32), random.randint(105, YUKSEKLIK - 150),
			                          self.balikListe[1], 1))
			self.balik_grup.add(Balik(random.randint(0, GENISLIK - 32), random.randint(105, YUKSEKLIK - 150),
			                          self.balikListe[2], 2))
			self.balik_grup.add(Balik(random.randint(0, GENISLIK - 32), random.randint(105, YUKSEKLIK - 150),
			                          self.balikListe[3], 3))

	def skor_kayit(self):
		skorTablosu.yazdir(self.skor, self.sure)
		# dbSkorlar.insert(self.skor, self.sure)

	def skor_cizdir(self):
		skorlar = skorTablosu.oku()
		# skorlar = dbSkorlar.select()
		alta_kaydir = 0
		# Arka Plan
		pencere.blit(self.oyun_arka_plan, (0, 0))
		# Skorlar Başlık Metni
		metin_skorlar_baslik = self.oyun_font.render("SKORLAR", True, (255, 255, 255), (0, 0, 170))
		metin_skorlar_baslik_konum = metin_skorlar_baslik.get_rect()
		metin_skorlar_baslik_konum.top = 30
		metin_skorlar_baslik_konum.left = 30
		pencere.blit(metin_skorlar_baslik, metin_skorlar_baslik_konum)
		for skor in skorlar:
			# Skorlar Metni
			metin_skorlar = self.oyun_font.render(skor, True, (255, 255, 255), (0, 0, 170))
			metin_skorlar_konum = metin_skorlar.get_rect()
			metin_skorlar_konum.top = 120 + alta_kaydir
			metin_skorlar_konum.left = 30

			# Skorları Çiz
			pencere.blit(metin_skorlar, metin_skorlar_konum)

			# Ekranı Güncelle
			pygame.display.update()
			alta_kaydir += 60


# Ana Karakter Grup İşlemleri
buyuk_balik_grup = pygame.sprite.Group()
buyuk_balik = BuyukBalik(GENISLIK // 2, YUKSEKLIK - 25)
buyuk_balik_grup.add(buyuk_balik)

# Baliklar Grup İşlemleri
balik_grup = pygame.sprite.Group()

# Oyun Sınıfı
oyun = Oyun(buyuk_balik, balik_grup)
oyun.hedefle()

# Oyun Döngüsü
durum = True
while durum:
	for etkinlik in pygame.event.get():
		if etkinlik.type == pygame.QUIT:
			durum = False
	pencere.fill((0, 0, 0))
	# Oyun Mekaniği
	oyun.update()
	oyun.cizdir()
	# Balıkçı Çizdirme ve Güncelleme
	buyuk_balik_grup.update()
	buyuk_balik_grup.draw(pencere)
	# Balık Çizdirme ve Güncelleme
	balik_grup.update()
	balik_grup.draw(pencere)
	pygame.display.update()
	saat.tick(FPS)

pygame.quit()
