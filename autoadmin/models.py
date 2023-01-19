from django.db import models
from django.utils.text import slugify
from io import BytesIO
from PIL import Image
from django.core.files import File

def compress(image):
    im = Image.open(image)
    if im.mode in ("RGBA", "P"): 
        im = im.convert("RGB")
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image

class Companie(models.Model):
    CUI = models.CharField(max_length=20, null=False, blank=False, primary_key=True)
    denumire = models.CharField(max_length=50, null=False, blank=False)
    nr_registru_comert = models.CharField(max_length=20, null=False, blank=False)
    adresa = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    telefon = models.CharField(max_length=200, null=False, blank=False)
    class Meta:
        verbose_name_plural = 'companie'
    def __str__(self):
        return self.denumire

class Categorie(models.Model):
    denumire = models.CharField(max_length=50, null=False, blank=False, unique=True) 
    class Meta:
        verbose_name_plural = 'categorie'
    def __str__(self):
        return self.denumire

class Marca(models.Model):
    denumire =  models.CharField(max_length=50, null=False, blank=False, unique=True) 
    class Meta:
        verbose_name_plural = 'marca'
        ordering = ['denumire']
    def __str__(self):
        return self.denumire

class Combustibil(models.Model):
    denumire =  models.CharField(max_length=50, null=False, blank=False, unique=True)
    class Meta:
        verbose_name_plural = 'combustibil'
    def __str__(self):
        return self.denumire

class Transmisie(models.Model):
    denumire =  models.CharField(max_length=50, null=False, blank=False, unique=True)
    class Meta:
        verbose_name_plural = 'transmisie'
    def __str__(self):
        return self.denumire

class CutieDeViteza(models.Model):
    denumire =  models.CharField(max_length=50, null=False, blank=False, unique=True)
    class Meta:
        verbose_name_plural = 'cutie de viteze'
    def __str__(self):
        return self.denumire

class Caroserie(models.Model):
    denumire =  models.CharField(max_length=50, null=False, blank=False, unique=True)
    class Meta:
        verbose_name_plural = 'caroserie'
    def __str__(self):
        return self.denumire

class NormaDePoluare(models.Model):
    denumire =  models.CharField(max_length=50, null=False, blank=False, unique=True)
    class Meta:
        verbose_name_plural = 'norma de poluare'
    def __str__(self):
        return self.denumire

class Stare(models.Model):
    denumire = models.CharField(max_length=50, null=False, blank=False, unique=True) 
    class Meta:
        verbose_name_plural = 'stare'
    def __str__(self):
        return self.denumire

class CategorieDotari(models.Model):
    denumire = models.CharField(max_length=100, null=False, blank=False, unique=True) 
    class Meta:
        verbose_name_plural = 'categorie dotari'
    def __str__(self):
        return self.denumire

class Dotare(models.Model):
    categorie_dotari = models.ForeignKey('CategorieDotari',on_delete=models.RESTRICT, null=False, blank=False)
    denumire = models.CharField(max_length=100, null=False, blank=False, unique=True) 

    def __str__(self):
        return f'{self.categorie_dotari.denumire} | {self.denumire}'
    
    class Meta:
        verbose_name_plural = 'dotari'
        ordering = ['categorie_dotari','denumire']

class Autovehicul(models.Model):
    categorie = models.ForeignKey('Categorie',on_delete=models.RESTRICT, null=False, blank=False)
    marca = models.ForeignKey('Marca',on_delete=models.RESTRICT, null=False, blank=False)
    model = models.CharField(max_length=100, null=False, blank=False)
    versiune = models.CharField(max_length=100, null=True, blank=True)
    titlu = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=150, unique=True)
    descriere = models.TextField(max_length=2000, null=True, blank=True)
    vizibil = models.BooleanField(null=False, default=True)
    vandut = models.BooleanField(null=False, default=False)
    an_fabricatie = models.SmallIntegerField(null=False,blank=False)
    km = models.IntegerField(null=False,blank=False)
    combustibil = models.ForeignKey('Combustibil',on_delete=models.RESTRICT, null=False, blank=False)
    putere =  models.SmallIntegerField(null=False,blank=False)
    capacitate_cilindrica = models.SmallIntegerField(null=False,blank=False)
    VIN = models.CharField(max_length=50, null=True, blank=True)
    transmisie = models.ForeignKey('Transmisie',on_delete=models.RESTRICT, null=False, blank=False)
    norma_de_poluare = models.ForeignKey('NormaDePoluare',on_delete=models.RESTRICT, null=False, blank=False)
    cutie_de_viteza = models.ForeignKey('CutieDeViteza',on_delete=models.RESTRICT, null=False, blank=False)
    consum_urban = models.CharField(max_length=50, null=True, blank=True)
    caroserie = models.ForeignKey('Caroserie',on_delete=models.RESTRICT, null=False, blank=False)
    numar_portiere = models.SmallIntegerField(null=False,blank=False)
    culoare = models.CharField(max_length=50, null=False,blank=False)
    optiuni_culoare = models.CharField(max_length=50, null=False,blank=False)
    stare = models.ForeignKey('Stare',on_delete=models.RESTRICT, null=False, blank=False)
    pret_euro = models.IntegerField(null=False, blank=False)
    garantie = models.CharField(max_length=100, null=True, blank=True)
    dotari = models.ManyToManyField('Dotare')
    data_adaugare = models.DateTimeField(auto_now_add=True)
    data_modificare = models.DateTimeField(auto_now=True)
    review_post_vanzare = models.TextField(max_length=2000, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'autovehicule'
        ordering = ['-id']

    def __str__(self):
        return f'{self.titlu} | {self.data_adaugare.date()}'
    
    def _generate_unique_slug(self):
        potential_slug = slugify(self.titlu)
        num = None
        while Autovehicul.objects.filter(slug=(potential_slug + '-' + str(num) if num else potential_slug)).exclude(pk=self.pk).exists():
            num = int(num or 1) + 1
        unique_slug = potential_slug + '-' + str(num) if num else potential_slug
        print(unique_slug)
        return unique_slug
    
    def save(self, *args, **kwargs):
        self.titlu = str(self.marca) + ' ' + str(self.model) + ' ' + str(self.versiune)
        self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        path = 'automobile-vandute' if self.vandut else 'auto'
        return f'/{path}/{self.slug}/'


class ImaginiAuto(models.Model):
    autovehicul = models.ForeignKey('Autovehicul', related_name="imagine_auto", on_delete=models.CASCADE)
    foto = models.ImageField("foto",upload_to='auto/images', max_length=200, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Autovehicule foto bulk upload'
        ordering=['id']

    def __str__(self):
        return self.autovehicul.titlu
    
    def save(self, *args, **kwargs):
            new_image = compress(self.foto)
            self.foto = new_image
            super().save(*args, **kwargs)