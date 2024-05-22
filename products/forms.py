from django import forms
from products.exceptions import ProductPriceDuplicateVariationException, ProductPriceMissingVariationException
from products.models import ProductPrice, Variation


class ProductPriceAdminForm(forms.ModelForm):
    class Meta:
        model = ProductPrice
        fields = '__all__'

    def clean(self):
        variation_options = self.cleaned_data.get('variation_option')
        variations = [vo.variation for vo in variation_options]
        if variations != list(set(variations)):
            raise ProductPriceDuplicateVariationException()

        variations = set(variations)
        product_variation = set(Variation.objects.filter(products=self.cleaned_data.get('product')))
        if variations != product_variation:
            raise ProductPriceMissingVariationException()

        return super(ProductPriceAdminForm, self).clean()
