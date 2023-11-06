import axios from 'axios';
import { API_URL } from '../config';
import authHeader from '../utils/authHeader';
import { CfaPricePrediction } from './models/CfaPricePrediction';
import { IBuyAdvice } from './models/IBuyAdvice';

class PredictionApiService {
    public async fetchCfaPricePrediction(cfaImageId: number): Promise<number[]> {
        const response = await axios.get<CfaPricePrediction>(
            `${API_URL}/cfa-image/pred-price/${cfaImageId}`,
            {
                headers: authHeader(),
            }
        );

        return response.data.predictions;
    }

    public async fetchBuyAdvice(cfaImageId: number): Promise<IBuyAdvice> {
        const response = await axios.get<IBuyAdvice>(
            `${API_URL}/cfa-image/buy-advice/${cfaImageId}`
        );

        return response.data;
    }
}

export const PredictionApiServiceInstanse = new PredictionApiService();
