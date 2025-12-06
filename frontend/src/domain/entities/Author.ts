export interface Author {
  id: number;
  name: string;
  surname: string;
  patronymic: string;
  bio: string;
  date_birth: string;
  date_death: string;
}

export interface AuthorPayload {
  name: string;
  surname: string;
  patronymic: string;
  bio: string;
  date_birth: string;
  date_death: string;
}






