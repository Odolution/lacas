import requests

from iteration_utilities import unique_everseen

# global variable


# student_dic ={}

class Fact_Api():
    student_data_list = list()
    data = {}
    def getstudentdata(self,fact_id,page_by_page):
        url = f"https://api.factsmgt.com/Students?Page={page_by_page}"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Es1KXmdfd3HW/L5pUdC5wIN/yE5ZQvnMbka3pPqvH0sig4fZrSKriKgsA1QPjsfJSU='
        }

        response = requests.request("GET", url, headers=headers, data=payload).json()
        result = response['results']
        for student in result:
            if fact_id == student.get('studentId'):
                self.student_data_list.append(student)
                self.data['student'] = student
                break
                # student_dic.extend(student)


    def getpickupdata(self,fact_id, page_by_page):
        url_pickup = f"https://api.factsmgt.com/students/PickupContacts?Page={page_by_page}"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Es1KXmdfd3HW/L5pUdC5wIN/yE5ZQvnMbka3pPqvH0sig4fZrSKriKgsA1QPjsfJSU='
        }
        response = requests.request("GET", url_pickup, headers=headers, data=payload).json()
        results = response['results']
        for pickup in results:

            # for family in family_data:
            if fact_id == pickup.get('studentId'):
                self.student_data_list.append(pickup)
                self.data['pickup'] = pickup
                break


    def getpeopledata(self,fact_id, page_by_page):
        url_person = f"https://api.factsmgt.com/people?Page={page_by_page}"
        # url = f"https://api.factsmgt.com/Students?Page={page_by_page}"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Es1KXmdfd3HW/L5pUdC5wIN/yE5ZQvnMbka3pPqvH0sig4fZrSKriKgsA1QPjsfJSU='
        }

        response = requests.request("GET", url_person, headers=headers, data=payload).json()
        results = response['results']
        for people in results:
            # for student in student_data:
                if fact_id == people.get('personId'):
                    self.student_data_list.append(people)
                    self.data['people'] = people
                    break

    #
    def getpersonfamilydata(self,fact_id, page_by_page):
        url_personfamily = f"https://api.factsmgt.com/people/PersonFamily?Page={page_by_page}"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Es1KXmdfd3HW/L5pUdC5wIN/yE5ZQvnMbka3pPqvH0sig4fZrSKriKgsA1QPjsfJSU='
        }

        response = requests.request("GET", url_personfamily, headers=headers, data=payload).json()
        results = response['results']
        for personfamily in results:
            # for person in poeple_data:
                if fact_id == personfamily.get('personId'):
                    self.student_data_list.append(personfamily)
                    self.data['personfamily'] = personfamily
                    break


    def getfamilydata(self,person_family_data, page_by_page):
        url_family = f"https://api.factsmgt.com/families?Page={page_by_page}"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Es1KXmdfd3HW/L5pUdC5wIN/yE5ZQvnMbka3pPqvH0sig4fZrSKriKgsA1QPjsfJSU='
        }
        response = requests.request("GET", url_family, headers=headers, data=payload).json()
        results = response['results']
        for family in results:
            for personfamily in person_family_data:

                if personfamily.get('familyId') == family.get('familyID'):
                    self.student_data_list.append(family)
                    self.data['family']=family
                    break


    def getdemographicdata(self,fact_id, page_by_page):
        url_demographic = f"https://api.factsmgt.com/people/Demographic?page={page_by_page}"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Es1KXmdfd3HW/L5pUdC5wIN/yE5ZQvnMbka3pPqvH0sig4fZrSKriKgsA1QPjsfJSU='
        }
        response = requests.request("GET", url_demographic, headers=headers, data=payload).json()
        results = response['results']
        for demo in results:
            # for personfamily in person_family_data:
                if fact_id == demo.get('personId'):
                    self.student_data_list.append(demo)
                    self.data['demographic']= demo
                    break



    def main(self,fact_id):
        for i in range(13):

            if i == 0:
                continue



            if i < 6:
                self.getstudentdata(fact_id,i)
                self.getpickupdata(fact_id,i)
            self.getpeopledata(fact_id, i)
            self.getpersonfamilydata(fact_id, i)
            self.getdemographicdata(fact_id, i)
            self.getfamilydata(self.student_data_list, i)
        finalstudent_data_list=list(unique_everseen([i for i in self.student_data_list]))
        return self.data


#remove duplication


