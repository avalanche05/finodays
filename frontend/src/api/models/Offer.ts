import { CfaImage } from '.';
import { User } from '../../models/User';

export interface Offer {
    cfa_image: CfaImage;
    count: number;
    id: number;
    price: number;
    seller: User;
}
