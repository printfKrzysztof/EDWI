describe('Laboratorium 3 - Cypress', () => {
  const surname = 'Wyczechowski'; // Zastąp 'Wyczechowski' odpowiednim nazwiskiem

  it('should find the surname, choose a person, and send a message', () => {
    // Wejdź na stronę
    cy.visit('https://adm.edu.p.lodz.pl/user/users.php');

    // Wpisz nazwisko w pole wyszukiwania
    cy.get('input[name="search"]').type(surname);
    cy.get('input[type="submit"][value="Wyszukaj w bazie wszystkich pracowników"]').click();

    // Czekaj na wyniki wyszukiwania
    cy.get('.userlist.userdetails').should('be.visible');

    // Lista wyników
    cy.get('.user-profile').then(profiles => {
      // Jeśli znaleziono więcej niż jedną osobę, wybierz pierwszą z listy
      if (profiles.length > 0) {
        // Wybierz pierwszą osobę z listy
        cy.wrap(profiles.first()).find('a').contains('Wyślij wiadomość').click();
      } else {
        // Jeśli nie znaleziono żadnej osoby, wyświetl komunikat
        cy.log('Nie znaleziono pracownika o podanym nazwisku.');
      }
    });

    // Upewnij się, że jesteśmy na stronie formularza kontaktowego
    cy.url().should('include', 'usermailform');

    // Wypełnij formularz kontaktowy
    cy.wait(500)
    cy.get('input[name="from"]').type('Krzysztof Bortnowski');
    cy.wait(500)
    cy.get('input[name="email"]').type('229538@edu.p.lodz.pl');
    cy.wait(500)
    cy.get('input[name="topic"]').type('Testy cypressa');
    cy.wait(500)
    cy.get('div[id="id_messageeditable"]').type('To jest testowa wiadomość.');

    cy.wait(1000)
    // Wyślij formularz
    cy.get('input[name="submitbutton"]').click();

    // Sprawdź, czy pojawił się komunikat "Wiadomość wysłana"
    cy.contains('Wiadomość wysłana').should('be.visible');
  });
});