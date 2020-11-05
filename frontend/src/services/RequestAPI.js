import axios from "axios";

export class RequestAPI {
  static get(model, queryParams) {
    const HOST = "http://127.0.0.1:8000/api";
    var endpoint = `${HOST}/${model}/?`;
    console.log(queryParams);
    for (const [key, value] of Object.entries(queryParams)) {
      if (value !== "") {
        endpoint += `${key}=${value}&`;
      }
    }
    return new Promise((resolve, reject) => {
      axios
        .get(endpoint)

        .then((response) => {
          console.log(response);
          if (response.status >= 400) {
            reject(Error(`${response.status} ${response.statusText}`));
          }
          resolve({ data: response.data });
        });
    });
  }
}
export default RequestAPI;
