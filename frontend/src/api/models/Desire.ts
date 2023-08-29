import { CfaImage } from '.';
import { User } from '../../models/User';

export interface Desire {
    cfa_image: CfaImage;
    count: number;
    id: number;
    price: number;
    seller: User;
}
