from rest_framework import status, permissions, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from services.ml_service import MLService
from core.permissions import IsFarmer, IsFarmerOrOfficer
from .models import PredictionHistory
from .serializers import PredictionInputSerializer, PredictionHistorySerializer
from .filters import PredictionHistoryFilter

class PredictView(APIView):
    permission_classes = (IsFarmer,)
    serializer_class = PredictionInputSerializer
    @extend_schema(
        summary="Run ML Crop Prediction",
        description="Predicts the most suitable crop and alternative options based on soil and weather parameters. Saves the output to user prediction history.",
        request=PredictionInputSerializer,
        responses={
            201: OpenApiResponse(
                description="Prediction calculated successfully.",
                examples=[
                    {
                        "predicted_crop": "Rice",
                        "confidence_score": 92.4,
                        "risk_level": "Low",
                        "recommendation": "Highly suitable conditions detected for Rice.",
                        "alternative_crops": [
                            {"crop": "Maize", "confidence": 84.5},
                            {"crop": "Wheat", "confidence": 78.2}
                        ]
                    }
                ]
            ),
            400: OpenApiResponse(description="Validation error with input parameters.")
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # Invoke ML engine
        ml_service = MLService()
        result = ml_service.predict(
            nitrogen=data['nitrogen'],
            phosphorus=data['phosphorus'],
            potassium=data['potassium'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            ph=data['ph'],
            rainfall=data['rainfall']
        )
        # Save to DB history
        PredictionHistory.objects.create(
            user=request.user,
            predicted_crop=result['predicted_crop'],
            confidence_score=result['confidence_score'],
            risk_level=result['risk_level'],
            nitrogen=data['nitrogen'],
            phosphorus=data['phosphorus'],
            potassium=data['potassium'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            ph=data['ph'],
            rainfall=data['rainfall']
        )
        return Response(result, status=status.HTTP_201_CREATED)
class PredictionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PredictionHistorySerializer
    permission_classes = (IsFarmerOrOfficer,)
    filterset_class = PredictionHistoryFilter
    search_fields = ('predicted_crop', 'user__email', 'user__full_name')
    ordering_fields = ('created_at', 'confidence_score')
    ordering = ('-created_at',)
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Farmer':
            # Farmers see only their own histories
            return PredictionHistory.objects.filter(user=user)
        # Officers and Admins see all histories
        return PredictionHistory.objects.all().select_related('user')
    @extend_schema(
        summary="List Prediction History",
        description="Lists past crop predictions. Farmers only see their own history, while Officers and Admins can see all. Supports filtering, searching, and pagination."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @extend_schema(
        summary="Retrieve Prediction Detail",
        description="Retrieves detail of a specific past crop prediction."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)