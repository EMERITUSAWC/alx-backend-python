cat > my_app/serializers.py << 'EOL'
from rest_framework import serializers
from datetime import date
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    days_since_published = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_days_since_published(self, obj):
        if obj.published_date:
            return (date.today() - obj.published_date).days
        return None  # or 0, depending on preference