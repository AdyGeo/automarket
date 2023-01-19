from rest_framework import serializers
from autoadmin.models import Autovehicul, Dotare, ImaginiAuto, Companie



class DotariSerializer(serializers.ModelSerializer):
    categorie_dotari = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    class Meta:
        model= Dotare
        fields='__all__'

class ImaginiAutoSerializer(serializers.ModelSerializer):
    class Meta:
        model= ImaginiAuto
        fields='__all__'

class CompanieSerializer(serializers.ModelSerializer):
    class Meta:
        model= Companie
        fields='__all__'

class AutovehiculSerializer(serializers.ModelSerializer):
    categorie = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    marca = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    combustibil = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    transmisie = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    norma_de_poluare = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    cutie_de_viteza = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    caroserie = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    stare = serializers.SlugRelatedField(many=False, read_only=True, slug_field="denumire")
    dotari = DotariSerializer(many=True, read_only=True)
    imagine_auto = ImaginiAutoSerializer(many=True, read_only=True)

    class Meta:
        model= Autovehicul
        fields='__all__'
