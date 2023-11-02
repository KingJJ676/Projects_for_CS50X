#include <cs50.h>
#include <stdio.h>
long cal_total(long cn);
void check_card(long cn);
long start_num_odd2(long cn);
long start_num_odd1(long cn);
long start_num_even(long cn);
long start_num_even1(long cn);

int main(void)
{
    //get user's card number
    long cn = get_long("Card number: ");

    //calculate total
    long sum = cal_total(cn);

    //check card length & starting digits
    check_card(cn);


}











////////////////////////////////////////
long cal_total(long cn)
{
    long sum1 = 0;
    long sum2 = 0;

    while (cn >= 10)
    {
        //get every other digit
        long last_num = cn % 10;
        cn = (cn - last_num) / 10;

        long second_last_num = cn % 10;
        cn = (cn - second_last_num) / 10;

        //get sum1
        if (second_last_num * 2 >= 10)
        {
            long last_num_2 = (second_last_num * 2) % 10;
            sum1 += last_num_2;
            long new_num = (second_last_num * 2 - last_num_2) / 10;
            sum1 += new_num;
        }

        else
        {
            sum1 += second_last_num * 2;
        }

         //get sum2
         sum2 += last_num;
    }

    long sn2 = start_num_odd2(cn);


    long total = 0;
    total = sum1 + sum2 + sn2;
    return total;
}

//////////////////////////////////////////
void check_card(long cn)
{
    //American Express
    if ((1e14 - 1) < cn && cn < 1e15 )
    {
        long sn1 = start_num_odd1(cn);
        long sn2 = start_num_odd2(cn);
        long sum = cal_total(cn) + sn1;

        if ((sum % 10 == 0) && (sn2 == 34 | sn2 == 37))
        {
            printf("AMEX\n");
            return;
        }
    }

    //Mastercard
    if ((1e15 - 1) < cn && cn < 1e16 )
    {
        long sn = start_num_even(cn);
        long sum = cal_total(cn);

        if ((sum % 10 == 0) && (sn == 51 | sn == 52 | sn == 53 | sn == 54 | sn == 55))
        {
            printf("MASTERCARD\n");
            return;
        }
    }

    //Visa13
    if ((1e12 - 1) < cn && cn < 1e13 )
    {
        long sn1 = start_num_odd1(cn);
        long sum = cal_total(cn) + sn1;

        if ((sum % 10 == 0) && (sn1 == 4))
        {
            printf("VISA\n");
            return;
        }
    }

    //visa16
    if ((1e15 - 1) < cn && cn < 1e16 )
    {
        long sn = start_num_even(cn);
        long sn1 = start_num_even1(cn);
        long sum = cal_total(cn);

        if ((sum % 10 == 0) && (sn1 == 4))
        {
            printf("VISA\n");
            return;
        }
    }

    //invalid
    printf("INVALID\n");
}















//////////////////////////////////////////
long start_num_odd2(long cn)
{
    long sn = 0;

    do
    {
        long last_num_4 = cn % 10;
        cn = (cn - last_num_4) / 10;

        long second_last_num_4 = cn % 10;
        cn = (cn - second_last_num_4) / 10;
    }
    while (cn > 1000);

    long last_num = cn % 10;
    cn = (cn - last_num) / 10;

    sn = cn;
    return sn;
}

long start_num_even(long cn)
{
    long sn = 0;

    do
    {
        long last_num_4 = cn % 10;
        cn = (cn - last_num_4) / 10;

        long second_last_num_4 = cn % 10;
        cn = (cn - second_last_num_4) / 10;
    }
    while (cn > 100);

    sn = cn;
    return sn;
}
////////////////////////////////////////
long start_num_even1(long cn)
{
    long sn = 0;

    do
    {
        long last_num_4 = cn % 10;
        cn = (cn - last_num_4) / 10;

        long second_last_num_4 = cn % 10;
        cn = (cn - second_last_num_4) / 10;
    }
    while (cn > 100);

    long last_num = cn % 10;
    cn = (cn - last_num) / 10;

    sn = cn;
    return sn;
}

////////////
long start_num_odd1(long cn)
{
    long sn = 0;

    do
    {
        long last_num_4 = cn % 10;
        cn = (cn - last_num_4) / 10;

        long second_last_num_4 = cn % 10;
        cn = (cn - second_last_num_4) / 10;
    }
    while (cn > 1000);

    long last_num = cn % 10;
    cn = (cn - last_num) / 10;
    long last_num2 = cn % 10;
    cn = (cn - last_num2) / 10;

    sn = cn;
    return sn;
}




