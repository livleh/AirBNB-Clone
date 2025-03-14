from rest_framework import serializers
from .models import Reservation
from datetime import date
from property.models import Property


class ReservationSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), required=True)
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        if data['start'] >= data['end']:
            raise serializers.ValidationError("End date must be after start date")
        
        if data['start'] < date.today():
            raise serializers.ValidationError("Reservation must be for a future date")
        
        # Check for overlap
        property = data['property']
        start = data['start']
        end = data['end']
        existing_reservations = Reservation.objects.filter(
            property=property,
            status__in=['P', 'A'],
            start__lt=end,
            end__gt=start,
        )
        if existing_reservations.exists():
            raise serializers.ValidationError("Reservation overlaps with existing reservation for this property")
        
        return data